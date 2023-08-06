from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
import pandas as pd
import os
import json
from randomlib.config import ROOT_DIR

class HateModel:
    Models = {}

    @classmethod
    def loadModels(cls):
        path = os.path.join(ROOT_DIR, 'modelsjson', 'hateModels.json')
        print(path)
        with open(path) as f:
            cls.Models = json.load(f)
        return cls.Models

            
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
        
    def listModels(self):
        modelElements = HateModel.Models
        for i in modelElements:
            print(i, ": ", modelElements[i], "\n")

HateModel.loadModels()