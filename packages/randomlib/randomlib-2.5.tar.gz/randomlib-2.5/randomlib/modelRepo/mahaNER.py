from transformers import BertTokenizerFast, BertForTokenClassification, TokenClassificationPipeline
from IPython.display import display
import torch
import logging
import pandas as pd
import os
import json
from randomlib.config import ROOT_DIR

################# LOGGING #################
nerPipeLogger = logging.getLogger(__name__)
consoleHandler = logging.StreamHandler()
logFormatter = logging.Formatter(fmt=' %(name)s :: %(levelname)-4s :: %(message)s')

nerPipeLogger.setLevel(logging.DEBUG)
consoleHandler.setLevel(logging.DEBUG)

consoleHandler.setFormatter(logFormatter)
nerPipeLogger.addHandler(consoleHandler)

################# LOGGING #################

class NERModel:
    Models = {}
    
    @classmethod
    def loadModels(cls):
        path = os.path.join(ROOT_DIR, 'modelsjson', 'nerModels.json')
        print(path)
        with open(path) as f:
            cls.Models = json.load(f)
        return cls.Models

    def __init__(self, modelName='marathi-ner',gpu_enabled:bool = False):
        self.modelName = modelName
        self.gpu_enabled = gpu_enabled
        self.device = 1 if (self.gpu_enabled and torch.cuda.is_available()) else -1

        try:
            self.pretrainedNERModel = BertForTokenClassification.from_pretrained(self.__class__.Models[self.modelName])
        except Exception as e:
            nerPipeLogger.exception(
                msg="some error has occured while Loading mahaNER_BERT Model", exc_info=e)
            return None

        try:
            self.NERTokenizer = BertTokenizerFast.from_pretrained(self.__class__.Models[self.modelName])
        except Exception as e:
            nerPipeLogger.exception(
                msg="some error has occured while Loading mahaNER_BERT Tokenizer", exc_info=e)
            return None

        self.pipeline = TokenClassificationPipeline(
            task='marathi-ner',
            model=self.pretrainedNERModel,
            tokenizer=self.NERTokenizer,
            framework="pt",
            aggregation_strategy='first',
            device=self.device,
        )

    def getPolarityScore(self, text, details: str = "minimum",as_dict:bool = False):
        '''
        text = A string of raw text as a input to NER model
        details = Defines the level of details to get from the prediction.
                possible values = 'minimum' (default),'medium','all'.
        as_dict = returns the raw result

        '''
        self.labels = pd.DataFrame(self.pipeline(text))

        self.labels['word'] = self.labels['word'].apply(lambda arr:list(arr.split(" ")))
        self.labels = self.labels.explode('word',ignore_index=True)
        columns = ['word','entity_group','score','start','end']

        if details == 'minimum':
            predicts = self.labels[columns[:2]]

        if details == "medium":
            predicts = self.labels[columns[:3]]

        if details == "all":
            predicts = self.labels[columns]

        with pd.option_context('display.max_rows', 10,
                       'display.max_columns', None,
                       'display.width', 1000,
                       'display.colheader_justify', 'left'):
            display(predicts)

        if as_dict:
            return predicts.to_dict('records')
        return predicts

    def getTokenLabels(self,text):
        predictions = self.pipeline(text)

        self.tokenLabels  = ""
        for token in predictions:
            subwords = list(token['word'].strip().split(" "))
            for _ in subwords:
                self.tokenLabels  = self.tokenLabels + (" "  + token['entity_group'])

        self.tokenLabels = self.tokenLabels.lstrip()
        return self.tokenLabels

    def listModels(self):
        modelElements = NERModel.Models
        for i in modelElements:
            print(i, ": ", modelElements[i], "\n")

NERModel.loadModels()