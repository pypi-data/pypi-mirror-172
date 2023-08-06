from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
import pandas as pd
import os
import json

class HateModel:
    Models = {}
    # {
    #     'mahahate-bert': 'l3cube-pune/mahahate-bert',
    #     'mahahate-multi-roberta': 'l3cube-pune/mahahate-multi-roberta'
    # }

    @classmethod
    def loadModels(cls):
        path = os.path.join(os.path.dirname(__file__), '..', 'modelsjson', 'hateModels.json')
        print(path)
        with open(path) as f:
            cls.Models = json.load(f)
        print('Models are: \n',cls.Models)

    def __init__(self, modelName='mahahate-bert'):
        self.modelName = modelName
        self.modelRoute = HateModel.Models[self.modelName]
        self.tokenizer = AutoTokenizer.from_pretrained(self.modelRoute)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.modelRoute)
        self.classifier = pipeline('text-classification',
                              model=self.model, tokenizer=self.tokenizer)

    def getPolarityScore(self, text):
        result = self.classifier(text)
        df = pd.DataFrame.from_dict(result)
        return df
        
    def listModels():
        modelElements = HateModel.Models
        for i in modelElements:
            print(i, ": ", modelElements[i], "\n")

HateModel.loadModels()