from chatbot import RuleBasedChatbot

def test_greeting(): assert RuleBasedChatbot().respond('Hello Sura!').intent == 'greetings'
def test_time_is_dynamic(): assert 'current time is' in RuleBasedChatbot().respond('What time is it?').text
def test_search_extracts_query():
    result = RuleBasedChatbot().respond('Search Google for artificial intelligence')
    assert result.command == 'search_google' and result.argument == 'artificial intelligence'
def test_unknown_command(): assert RuleBasedChatbot().respond('do something unsafe').intent == 'unknown'
