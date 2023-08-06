from randomlib.modelRepo.mahaHate import HateModel

Models = {
        'mahahate-bert': 'l3cube-pune/mahahate-bert',
        'mahahate-multi-roberta': 'l3cube-pune/mahahate-multi-roberta'
}

class HateAnalyzer(HateModel):
    def __init__(self, modelName = 'mahahate-bert'):
        self.modelName = modelName
        super().__init__(self.modelName)

    def getPolarityScore(self, text):
        return super().getPolarityScore(text)

def listModels():
    modelElements = Models
    print("Hate Speech Models: ")
    for i in modelElements:
        print(i, ": ", modelElements[i], "\n")


