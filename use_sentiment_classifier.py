from afinn import Afinn

class SentimentClassifier:
    def __init__(self, friendly_threshold=2, hostile_threshold=-2):
        self.afinn = Afinn()
        self.friendly_threshold = friendly_threshold
        self.hostile_threshold = hostile_threshold

    def classify(self, text):
        score = self.afinn.score(text)
        if score > self.friendly_threshold:
            return "friendly"
        elif score < self.hostile_threshold:
            return "hostile"
        else:
            return "neutral"

    def get_score(self, text):
        return self.afinn.score(text)


if __name__ == "__main__":
    classifier = SentimentClassifier()

    texts = [
        "I absolutely love this!",
        "You're terrible at your job.",
        "That was okay, I guess.",
        "Thanks a lot for your help!",
        "Why would you even say something like that?"
    ]

    for text in texts:
        score = classifier.get_score(text)
        label = classifier.classify(text)
        print(f"Text: '{text}'\nScore: {score:.2f} → {label}\n")
