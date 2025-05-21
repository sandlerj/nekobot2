# The following was written/edited using AI

import asyncio
from bot.bot import NekoBot
from dotenv import load_dotenv
import logging

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
        
        # Initialize and start the bot
        bot = NekoBot()
        await bot.start()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    asyncio.run(main())