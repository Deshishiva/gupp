
class MemoryExtractor:
    def run(self, messages):
        text = " ".join([m.content.lower() for m in messages])
        prefs, emos, facts = [], [], {}

        if "ai" in text: prefs.append("interested in AI")
        if "job" in text: prefs.append("career seeking")
        if "help" in text: emos.append("seeking support")

        return {
            "preferences": prefs,
            "emotional_patterns": emos,
            "facts_to_remember": facts
        }
