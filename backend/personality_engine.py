
class PersonalityEngine:
    def apply(self, persona, text):
        if persona == "Calm Mentor":
            return "🧘 Calm Mentor: " + text
        if persona == "Witty Friend":
            return "😄 Witty Friend: " + text
        if persona == "Therapist":
            return "🪴 Therapist: " + text
        return text
