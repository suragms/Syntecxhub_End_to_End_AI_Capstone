from .rule_engine import RuleBasedChatbot
class IntentClassifier:
    def __init__(self): self.engine = RuleBasedChatbot()
    def classify(self, text): return self.engine.respond(text).intent
