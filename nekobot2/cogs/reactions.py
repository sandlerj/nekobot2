# The following was written/edited using AI

import discord
from discord.ext import commands
import logging
from services.image_api import ImageAPIService
from services.trigger_matcher import TriggerMatcher
from typing import Dict, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ReactionHandler(commands.Cog):
    """Handles reaction commands and keyword triggers"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = bot.config
        self.image_service = ImageAPIService(self.config)
        self.trigger_matcher = TriggerMatcher(self.config)
        self.muted_until: Optional[datetime] = None
        
    async def cog_load(self):
        """Initialize services when cog is loaded"""
        await self.image_service.initialize()
        
    async def cog_unload(self):
        """Cleanup services when cog is unloaded"""
        await self.image_service.cleanup()
        
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Listen for messages and respond to triggers"""
        # Ignore bot messages
        if message.author.bot:
            return
        
        if self.muted_until and datetime.now() < self.muted_until:
            return
            
        # Check for trigger matches
        matches = await self.trigger_matcher.find_matches(message.content)
        for match in matches:
            await self._send_reaction(message, match.reaction_type)
            break  # Only send one reaction per message
                
    async def _send_reaction(self, message: discord.Message, reaction_type: str):
        """Send a reaction image for the given type"""
        try:
            image_url = await self.image_service.get_image(reaction_type)
            if image_url:
                embed = discord.Embed(color=discord.Color.random())
                embed.set_image(url=image_url)
                await message.channel.send(embed=embed)
            else:
                logger.warning(f"No image URL found for reaction type: {reaction_type}")
        except Exception as e:
            logger.error(f"Error sending reaction: {e}")
    
    @commands.command(name="be-quiet")
    async def be_quiet(self, ctx: commands.Context, waitTime: Optional[int]):
        """Mutes the bot for given seconds"""
        wait_seconds = waitTime if waitTime != None else self.config.get("cooldown", {}).get("global", 30)
        self.muted_until = datetime.now() + timedelta(seconds=wait_seconds)
        await ctx.send(f"I'll be quiet for {wait_seconds} seconds :(")

    @commands.command(name="triggers")
    async def list_triggers(self, ctx: commands.Context):
        """List all available reaction triggers"""
        triggers_by_type = {}
        for trigger, reaction_type in self.reaction_triggers.items():
            if reaction_type.startswith("trap"): 
                continue
            if reaction_type not in triggers_by_type:
                triggers_by_type[reaction_type] = []
            triggers_by_type[reaction_type].append(trigger)
            
        embed = discord.Embed(
            title="Available Reaction Triggers",
            color=discord.Color.blue()
        )
        
        for reaction_type, triggers in triggers_by_type.items():
            embed.add_field(
                name=reaction_type.capitalize(),
                value=", ".join(f"`{t}`" for t in triggers),
                inline=False
            )
            
        await ctx.send(embed=embed)

    @commands.command(name="neko-help")
    async def reactions_help(self, ctx: commands.Context):
        """Shows detailed help about reaction commands and features"""
        embed = discord.Embed(
            title="Reactions Help",
            description="This bot responds to certain trigger words with reaction images!",
            color=discord.Color.blue()
        )

        # Commands section
        commands_text = (
            "`!neko-help` - Shows this help message\n"
            "`!triggers` - Lists all available reaction triggers\n"
            "`!be-quiet [seconds]` - Mutes reactions for specified seconds (default: 30)"
        )
        embed.add_field(
            name="Commands",
            value=commands_text,
            inline=False
        )

        # How it works section
        usage_text = (
            "Simply include any trigger word in your message and "
            "the bot will respond with a matching reaction image!\n"
            "For example, saying 'headpat' will trigger a patting reaction."
        )
        embed.add_field(
            name="How it Works",
            value=usage_text,
            inline=False
        )

        # Add reaction categories
        categories = set(filter(lambda x: x != "trap", self.reaction_triggers.values()))
        categories_text = ", ".join(f"`{cat}`" for cat in categories)
        embed.add_field(
            name="Available Reaction Types",
            value=categories_text,
            inline=False
        )

        embed.set_footer(text="Use !triggers to see all trigger words")
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    """Set up the reaction handler cog. This is an entrypoint required by 
    commands.Bot.load_extension"""
    await bot.add_cog(ReactionHandler(bot))