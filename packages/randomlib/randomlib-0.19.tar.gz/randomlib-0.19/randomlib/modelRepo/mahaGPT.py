from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import pipeline
import pandas as pd 

class GPTModel:
    Models = {
        'marathi-gpt': 'l3cube-pune/marathi-gpt'
    }

    def __init__(self, modelName='marathi-gpt'):
        self.modelName = modelName
        self.modelRoute = GPTModel.Models[self.modelName]
        self.tokenizer = AutoTokenizer.from_pretrained(self.modelRoute)
        self.model = AutoModelForCausalLM.from_pretrained(self.modelRoute)
        self.classifier = pipeline('text-generation',
                              model=self.model, tokenizer=self.tokenizer)

    def nextWord(self, text, numOfPredictions = 1):
        result = self.classifier(text, max_new_tokens = 1, num_return_sequences = numOfPredictions)
        df = pd.DataFrame.from_dict(result)
        # print(df)
        return df
    
    def completeSentence(self, text, numOfWords = 25, numOfPredictions = 1):
        result = self.classifier(text, max_new_tokens = numOfWords, num_return_sequences = numOfPredictions)
        df = pd.DataFrame.from_dict(result)
        # print(df)
        return df

    def listModels():
        modelElements = GPTModel.Models
        for i in modelElements:
            print(i, ": ", modelElements[i], "\n")