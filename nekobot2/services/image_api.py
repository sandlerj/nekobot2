# The following was written/edited using AI

import aiohttp
import logging
import random
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class ImageAPIService:
    """Service for fetching images from various anime image APIs"""
    
    def __init__(self, config: Dict):
        """Initialize with API configuration"""
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def initialize(self):
        """Create aiohttp session"""
        self.session = aiohttp.ClientSession()
        
    async def cleanup(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()
            
    async def get_image(self, reaction_type: str) -> Optional[str]:
        """Fetch an image URL for the given reaction type"""
        apis = ['nekos_life', 'waifu_pics']  # List of available APIs
        random.shuffle(apis)  # Randomize API selection for load distribution
        
        for api_name in apis:
            try:
                api_config = self.config.get('apis', {}).get(api_name, {})
                if not api_config:
                    continue
                    
                base_url = api_config.get('base_url')
                endpoint = api_config.get('endpoints', {}).get(reaction_type)
                
                if not (base_url and endpoint):
                    continue
                    
                url = f"{base_url}{endpoint}"
                async with self.session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Handle different API response formats
                        if api_name == 'nekos_life':
                            return data.get('url')
                        elif api_name == 'waifu_pics':
                            return data.get('url')
                            
            except Exception as e:
                logger.error(f"Error fetching image from {api_name}: {e}")
                continue
                
        return None