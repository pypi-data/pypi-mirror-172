from randomlib.modelRepo.mahaGPT import GPTModel

Models = {
        'marathi-gpt': 'l3cube-pune/marathi-gpt'
}

class TextGenerator(GPTModel):
    def __init__(self, modelName = 'marathi-gpt'):
        self.modelName = modelName
        super().__init__(self.modelName)

    def nextWord(self, text, numOfPredictions = 1):
        return super().nextWord(text, numOfPredictions = 1)

    def completeSentence(self, text, numOfWords = 25, numOfPredictions = 1):
        return super().completeSentence(text, numOfWords = 25, numOfPredictions = 1)


def listModels():
    modelElements = Models
    print("GPT Models: ")
    for i in modelElements:
        print(i, ": ", modelElements[i], "\n")
