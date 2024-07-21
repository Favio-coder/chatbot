# tests/test_stories.py

import pytest
from rasa.test import test_core 

@pytest.mark.parametrize("story_file", ["stories.md"])
def test_stories(story_file):
    failures = test_core(story_file)
    assert failures == 0, f"Found {failures} failed stories"
