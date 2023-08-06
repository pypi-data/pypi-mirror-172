from randomlib.modelRepo.mahaGPT import GPTModel

class TextGenerator(GPTModel):
    Models = {}
    @classmethod
    def loadModels(cls):
        cls.Models = super().loadModels()

    def __init__(self, modelName = 'marathi-gpt'):
        self.modelName = modelName
        super().__init__(self.modelName)

    def nextWord(self, text, numOfPredictions = 1):
        return super().nextWord(text, numOfPredictions)

    def completeSentence(self, text, numOfWords = 25, numOfPredictions = 1):
        return super().completeSentence(text, numOfWords, numOfPredictions )

    def listModels(self):
        return super().listModels()

TextGenerator.loadModels()