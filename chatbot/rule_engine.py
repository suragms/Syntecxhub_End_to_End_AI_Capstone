import json
import re
from datetime import datetime
from pathlib import Path
from core.models import ChatResponse

class RuleBasedChatbot:
    def __init__(self, intents_path=None):
        path = Path(intents_path or Path(__file__).with_name('intents.json'))
        self.intents = json.loads(path.read_text(encoding='utf-8'))

    @staticmethod
    def normalize(text):
        return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9\s]', ' ', text.lower())).strip()

    def respond(self, text):
        value = self.normalize(text)
        if not value:
            return ChatResponse('Please type a command so I can help.', 'empty')
        if value.startswith('search for '):
            query = value[11:]
            return ChatResponse(f"I'll search Google for {query}", 'search_google', 'search_google', query)
        if value.startswith('search google for '):
            query = value[18:]
            return ChatResponse(f"I'll search Google for {query}", 'search_google', 'search_google', query)
        for intent, phrases in self.intents.items():
            if any(value == self.normalize(phrase) for phrase in phrases):
                return self._response(intent, value)
        return ChatResponse("I don't recognize that command yet. Say 'help' to see supported commands.", 'unknown')

    def _response(self, intent, value):
        if intent == 'greetings': return ChatResponse('Hello! Welcome to SURA AI. How can I help you today?', intent)
        if intent == 'assistant_info': return ChatResponse('I am SURA AI, a local smart personal assistant developed by Surag M S for Syntecxhub.', intent)
        if intent == 'help': return ChatResponse('You can ask me to open approved apps or websites, search Google, tell the time or date, and end the session.', intent)
        if intent == 'time': return ChatResponse(datetime.now().strftime('The current time is %I:%M %p.'), intent)
        if intent == 'date': return ChatResponse(datetime.now().strftime("Today's date is %B %d, %Y."), intent)
        if intent == 'day': return ChatResponse(datetime.now().strftime('Today is %A.'), intent)
        if intent.startswith('open_'): return ChatResponse(f'Sure, opening {intent[5:].replace("_", " ").title()}.', intent, intent)
        if intent == 'search_google': return ChatResponse('Opening Google search results.', intent, intent, value)
        if intent == 'logout': return ChatResponse('Logging out of SURA AI.', intent, intent)
        if intent == 'exit': return ChatResponse('Closing the assistant.', intent, intent)
        if intent == 'stop_listening': return ChatResponse('Voice listening stopped. You can continue with text commands.', intent, intent)
        return ChatResponse('I can help with that.', intent)
