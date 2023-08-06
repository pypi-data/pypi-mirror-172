from randomlib.modelRepo.mahaNER import NERModel

Models = {
    'marathi-ner': 'l3cube-pune/marathi-ner'
}

class EntityRecognizer(NERModel):
    def __init__(self,modelName:str = 'marathi-ner',
                gpu_enabled: bool=False) -> None:
        self.modelName = modelName
        super().__init__(self.modelName,gpu_enabled)

    def getPolarityScore(self, text, details: str = "minimum", as_dict: bool = False):
        return super().getPolarityScore(text, details, as_dict)

    def getTokenLabels(self, text):
        return super().getTokenLabels(text)


def listModels():
    modelElements = Models
    print("NER Models: ")
    for i in modelElements:
        print(i, ": ", modelElements[i], "\n")
