# Enhanced Trigger Word Matching Implementation Plan

## 1. Overview
This document outlines the implementation plan for enhancing the trigger word matching system in Nekobot2. The goal is to make the matching system more sophisticated, reducing false positives while catching more valid triggers.

## 2. New Dependencies
Add to requirements.txt:
```txt
rapidfuzz>=3.0.0  # For improved fuzzy matching
```

## 3. Configuration Changes

### 3.1 Enhanced Config Structure
Update config.yaml to support new matching features:

```yaml
matching:
    fuzzy_threshold: 0.85      # Minimum similarity score for fuzzy matches
    use_regex: true           # Enable regex pattern matching
    max_word_distance: 3      # Max words between context terms
    
reactions:
  pat:
    triggers:
      text: "pat"
      context_words: ["head", "gently", "softly"]
      fuzzy_match: true
      regex_pattern: "\\b(?:head)?pat(?:ted|ting)?s?\\b"
    
    aliases:
      - "pet"
      - "pats"
      - "patpat"
    
    settings:
      require_context: false  # Whether context words are required
      priority: 1            # Higher priority matches are checked first
```

## 4. Implementation Phases

### Phase 1: Core Matching Infrastructure
1. Create new module `nekobot2/services/trigger_matcher.py`:
   - Implement TriggerMatcher class
   - Add basic pattern matching for trigger words and aliases. 
      > Enhanced matching will be added in phase two. Fuzzy matching, regex, and context aware matching do not need to be implemented in phase one but can left as TODOs in the code for future work.
   - Create unit test suite and add unit tests.

2. Update ReactionHandler:
   - Integrate new TriggerMatcher
   - Update trigger loading
   - Add configuration validation

### Phase 2: Enhanced Matching Features

#### 2.1 Fuzzy Matching
- Implement using rapidfuzz library
- Add similarity scoring
- Configure thresholds
- Add performance optimizations

#### 2.2 Regex Support
- Add regex pattern compilation
- Implement pattern matching
- Add validation system
- Create common pattern library

#### 2.3 Context Awareness
- Implement context word detection
- Add proximity scoring
- Create context validation
- Add configuration options

### Phase 3: Testing & Optimization

#### 3.1 Testing Infrastructure
- Create comprehensive test suite
- Add benchmark system
- Implement performance monitoring
- Create test data sets

#### 3.2 Performance Optimization
- Implement caching system
- Add pattern precompilation
- Optimize matching order
- Add early exit conditions

## 5. Technical Details

### 5.1 TriggerMatcher Class Structure
```python
class TriggerMatcher:
    def __init__(self, config: dict):
        self.config = config
        self.compiled_patterns = {}
        self.fuzzy_matcher = None
        self.context_validator = None
        
    async def initialize(self):
        """Compile patterns and initialize matchers"""
        
    async def find_matches(self, content: str) -> list[Match]:
        """Find all matching triggers in content"""
        
    def _check_fuzzy_matches(self, word: str) -> list[Match]:
        """Find fuzzy matches for a word"""
        
    def _check_regex_matches(self, content: str) -> list[Match]:
        """Find regex pattern matches"""
        
    def _validate_context(self, match: Match, content: str) -> bool:
        """Validate match has proper context"""
```

### 5.2 Match Result Structure
```python
@dataclass
class Match:
    trigger: str
    reaction_type: str
    confidence: float
    context_score: float
    matched_text: str
    start_pos: int
    end_pos: int
```

## 6. Migration Plan

1. Create new branch `feature/enhanced-triggers`
2. Implement core infrastructure
3. Add new configuration format
4. Create migration script for old configs
5. Add compatibility layer
6. Test extensively
7. Create documentation
8. Review and merge

## 7. Testing Strategy

### 7.1 Unit Tests
- Pattern compilation
- Fuzzy matching
- Context validation
- Configuration loading

### 7.2 Integration Tests
- Full matching pipeline
- Configuration integration
- Performance benchmarks
- Memory usage tests

### 7.3 Test Cases
- Common trigger variations
- Similar but invalid words
- Context combinations
- Edge cases
- Performance scenarios

## 8. Documentation

### 8.1 Technical Documentation
- Architecture overview
- Class documentation
- Configuration guide
- Performance guidelines

### 8.2 User Documentation
- Configuration examples
- Best practices
- Troubleshooting guide
- Migration guide

## 9. Timeline
1. Core Infrastructure: 2 days
2. Enhanced Features: 3 days
3. Testing & Optimization: 2 days
4. Documentation: 1 day
5. Review & Fixes: 1 day

Total: ~9 days

## 10. Success Metrics
- Reduced false positives by 90%
- Increased valid trigger detection by 50%
- Pattern matching under 1ms
- Memory usage under 10MB
- Test coverage > 90%
