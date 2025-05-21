# The following was written/edited using AI

import discord
from discord.ext import commands
import logging
from services.image_api import ImageAPIService
from typing import Dict, Set
from datetime import datetime, timedelta 
from typing import Optional

logger = logging.getLogger(__name__)

class ReactionHandler(commands.Cog):
    """Handles reaction commands and keyword triggers"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = bot.config
        self.image_service = ImageAPIService(self.config)
        self.reaction_triggers: Dict[str, Set[str]] = {}
        self.muted_until: Optional[datetime] = None
        self._load_triggers()
        
    def _load_triggers(self):
        """Load reaction triggers from config"""
        reactions = self.config.get('reactions', {})
        for reaction_type, triggers in reactions.items():
            for trigger in triggers:
                self.reaction_triggers[trigger.lower()] = reaction_type
    
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
            
        # Check message content against triggers
        words = message.content.lower().split()
        for word in words:
            if word in self.reaction_triggers:
                reaction_type = self.reaction_triggers[word]
                await self._send_reaction(message, reaction_type)
                break
                
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
        """Mutes the bot for 30 seconds"""
        wait_seconds = waitTime if waitTime != None else self.config.get("cooldown", {}).get("global", 30)
        self.muted_until = datetime.now() + timedelta(seconds=wait_seconds)
        await ctx.send(f"I'll be quiet for {wait_seconds} seconds :(")

    @commands.command(name="triggers")
    async def list_triggers(self, ctx: commands.Context):
        """List all available reaction triggers"""
        triggers_by_type = {}
        for trigger, reaction_type in self.reaction_triggers.items():
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

async def setup(bot: commands.Bot):
    """Set up the reaction handler cog. This is an entrypoint required by 
    commands.Bot.load_extension"""
    await bot.add_cog(ReactionHandler(bot))