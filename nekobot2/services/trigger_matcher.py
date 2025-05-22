# The following was written/edited using AI

from dataclasses import dataclass
from typing import Dict, List, Optional, Set
import logging

logger = logging.getLogger(__name__)

@dataclass
class Match:
    """Represents a matched trigger word with metadata"""
    trigger: str
    reaction_type: str
    confidence: float = 1.0
    context_score: float = 1.0
    matched_text: str = ""
    start_pos: int = -1
    end_pos: int = -1

class TriggerMatcher:
    """Handles detection and matching of trigger words in messages"""
    
    def __init__(self, config: dict):
        """Initialize the trigger matcher with configuration
        
        Args:
            config: Dict containing trigger word configuration
        """
        self.config = config
        self.triggers: Dict[str, Set[str]] = {}  # Maps trigger words to reaction types
        self._load_triggers()
        
    def _load_triggers(self) -> None:
        """Load trigger words from config into internal mapping"""
        reactions = self.config.get('reactions', {})
        
        for reaction_type, reaction_config in reactions.items():
            # Get main trigger word
            triggers = reaction_config.get('triggers', {})
            if isinstance(triggers, dict):
                trigger_text = triggers.get('text', '')
                if trigger_text:
                    self._add_trigger(trigger_text, reaction_type)
            
            # Get aliases - Fix: Actually add the aliases to triggers
            aliases = reaction_config.get('aliases', [])
            for alias in aliases:
                self._add_trigger(alias, reaction_type)
                
    def _add_trigger(self, trigger: str, reaction_type: str) -> None:
        """Add a trigger word to internal mapping
        
        Args:
            trigger: The trigger word/phrase
            reaction_type: The type of reaction this trigger should produce
        """
        trigger = trigger.lower()  # Convert to lowercase for case-insensitive matching
        if trigger not in self.triggers:
            self.triggers[trigger] = set()
        self.triggers[trigger].add(reaction_type)
        logger.debug(f"Added trigger '{trigger}' for reaction type '{reaction_type}'")
        
    async def find_matches(self, content: str) -> List[Match]:
        """Find all trigger word matches in the given content
        
        Args:
            content: The message content to check for triggers
            
        Returns:
            List of Match objects for any triggers found
        """
        matches = []
        content = content.lower()  # Convert to lowercase for case-insensitive matching
        words = content.split()
        
        for word in words:
            if word in self.triggers:
                for reaction_type in self.triggers[word]:
                    start_pos = content.find(word)
                    match = Match(
                        trigger=word,
                        reaction_type=reaction_type,
                        matched_text=word,
                        start_pos=start_pos,
                        end_pos=start_pos + len(word)
                    )
                    matches.append(match)
                    
        return matches

    # TODO: Phase 2 enhancements
    def _check_fuzzy_matches(self, word: str) -> List[Match]:
        """Find fuzzy matches for a word"""
        pass
        
    def _check_regex_matches(self, content: str) -> List[Match]:
        """Find regex pattern matches"""
        pass
        
    def _validate_context(self, match: Match, content: str) -> bool:
        """Validate match has proper context"""
        pass
