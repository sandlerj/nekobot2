# The following was written/edited using AI

import pytest
from nekobot2.services.trigger_matcher import TriggerMatcher, Match

@pytest.fixture
def basic_config():
    return {
        'reactions': {
            'pat': {
                'triggers': {'text': 'pat'},
                'aliases': ['pet', 'pats']
            },
            'hug': {
                'triggers': {'text': 'hug'},
                'aliases': ['hugs', 'cuddle']
            }
        }
    }

@pytest.fixture
def matcher(basic_config):
    return TriggerMatcher(basic_config)

def test_load_triggers(matcher):
    """Test that triggers are correctly loaded from config"""
    assert 'pat' in matcher.triggers
    assert 'pet' in matcher.triggers
    assert 'pats' in matcher.triggers
    assert 'hug' in matcher.triggers
    assert 'hugs' in matcher.triggers
    assert 'cuddle' in matcher.triggers

@pytest.mark.asyncio
async def test_find_matches_basic(matcher):
    """Test basic trigger word matching"""
    content = "I want to pat the cat"
    matches = await matcher.find_matches(content)
    assert len(matches) == 1
    assert matches[0].trigger == "pat"
    assert matches[0].reaction_type == "pat"

@pytest.mark.asyncio
async def test_find_matches_alias(matcher):
    """Test matching works with aliases"""
    content = "Time to give pets"
    matches = await matcher.find_matches(content)
    assert len(matches) == 1
    assert matches[0].trigger == "pet"
    assert matches[0].reaction_type == "pat"

@pytest.mark.asyncio
async def test_find_matches_multiple_triggers(matcher):
    """Test that multiple triggers in one message are found"""
    content = "hugs and pats for everyone"
    matches = await matcher.find_matches(content)
    assert len(matches) == 2
    triggers = {m.trigger for m in matches}
    assert "hugs" in triggers
    assert "pats" in triggers

@pytest.mark.asyncio
async def test_find_matches_case_insensitive(matcher):
    """Test that matching is case insensitive"""
    content = "PAT the CAT"
    matches = await matcher.find_matches(content)
    assert len(matches) == 1
    assert matches[0].trigger == "pat"
    assert matches[0].reaction_type == "pat"

@pytest.mark.asyncio
async def test_find_matches_no_match(matcher):
    """Test that no matches are found when no triggers present"""
    content = "Just a normal message"
    matches = await matcher.find_matches(content)
    assert len(matches) == 0
