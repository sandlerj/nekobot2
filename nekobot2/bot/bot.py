# The following was written/edited using AI

import os
import logging
import discord
from discord.ext import commands
from services.config_loader import ConfigLoader

logger = logging.getLogger(__name__)

class NekoBot(commands.Bot):
    """Main bot class for Nekobot that handles Discord events and commands"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize the bot with required intents and command prefix"""
        self.config_loader = ConfigLoader(config_path=config_path)
        self.config = self.config_loader.load_config()
        
        intents = discord.Intents.default()
        intents.message_content = True  # Required for message content access
        
        super().__init__(
            command_prefix=self.config_loader.get_prefix(),
            intents=intents,
            description=self.config.get('bot', {}).get('description')
        )
    
    async def setup_hook(self):
        """Initialize bot settings and load cogs"""
        logger.info("Setting up bot...")
        # Load reactions cog
        await self.load_extension("cogs.reactions")
        logger.info("Loaded reactions cog")
        
    async def on_ready(self):
        """Called when the bot has successfully connected to Discord"""
        logger.info(f"Logged in as {self.user.name} (ID: {self.user.id})")
        logger.info("------")
    
    async def start(self):
        """Start the bot with the token from environment variables"""
        token = os.getenv("DISCORD_TOKEN")
        if not token:
            raise ValueError("No Discord token found in environment variables")
        
        logger.info("Starting bot...")
        await super().start(token)