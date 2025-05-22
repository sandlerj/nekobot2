# The following was written/edited using AI

import asyncio
from bot.bot import NekoBot
from dotenv import load_dotenv
import logging
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Initialize and run the bot with configuration and error handling"""
    try:
        # Load environment variables
        load_dotenv()
        
        # Get config path from command line or use default
        config_path = sys.argv[1] if len(sys.argv) > 1 else "config/config.yaml"

        # Initialize and start the bot
        bot = NekoBot(config_path=config_path)
        await bot.start()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    asyncio.run(main())