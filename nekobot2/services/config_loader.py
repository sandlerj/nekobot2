# The following was written/edited using AI

import yaml
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ConfigLoader:
    """Service for loading and managing bot configuration"""

    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize the config loader with path to config file"""
        self.config_path = Path(config_path)
        self.config = {}

    def load_config(self) -> dict:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            logger.info("Configuration loaded successfully")
            return self.config
        except FileNotFoundError:
            logger.error(f"Configuration file not found at {self.config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error parsing configuration: {e}")
            raise

    def get_prefix(self) -> str:
        """Get bot command prefix"""
        return self.config.get('bot', {}).get('prefix', '!')

    def get_cooldown(self, cooldown_type: str) -> int:
        """Get cooldown value for specified type"""
        return self.config.get('cooldown', {}).get(cooldown_type, 0)

    def get_reactions(self) -> dict:
        """Get reaction trigger words mapping"""
        return self.config.get('reactions', {})

    def get_api_config(self, api_name: str) -> dict:
        """Get configuration for specified API"""
        return self.config.get('apis', {}).get(api_name, {})