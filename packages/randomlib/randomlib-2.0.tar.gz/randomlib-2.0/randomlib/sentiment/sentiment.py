from randomlib.modelRepo.mahaSentiment import SentimentModel

Models = {
        'MarathiSentiment': 'l3cube-pune/MarathiSentiment'
}

class SentimentAnalyzer(SentimentModel):
    def __init__(self, modelName = 'MarathiSentiment'):
        self.modelName = modelName
        super().__init__(self.modelName)

    def getPolarityScore(self, text):
        return super().getPolarityScore(text)

def listModels():
    modelElements = Models
    print("Sentiment Analysis Models: ")
    for i in modelElements:
        print(i, ": ", modelElements[i], "\n")


