import json
from utils import is_chat_event, is_resolved_event

def test_is_chat_event():
    with open('agent_allocator/tests/chat.json') as f:
        data = json.load(f)
    assert is_chat_event(data) == True

def test_is_resolved_event():
    with open('agent_allocator/tests/resolved.json') as f:
        data = json.load(f)
    assert is_resolved_event(data) == True
