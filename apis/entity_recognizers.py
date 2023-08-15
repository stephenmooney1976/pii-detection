#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 14:16:42 2023

@author: Stephen Mooney
"""

from presidio_analyzer import EntityRecognizer, RecognizerResult
from transformers import pipeline

# implement EntityRecognizer class for HuggingFace NER model
class TransformerRecognizer(EntityRecognizer):
    '''
    '''
    def __init__(
        self,
        model_id_or_path=None,
        aggregation_strategy='simple',
        supported_language='en',
        ignore_labels=['0','O','MISC']
    ):
         # initialize transformers pipeline for given mode or path
        self.pipeline = pipeline(
            "token-classification",
            model=model_id_or_path,
            aggregation_strategy=aggregation_strategy,
            ignore_labels=ignore_labels
        )

        # map labels to presidio labels
        self.label2presidio = {
            "PER": "PERSON",
            "LOC": "LOCATION",
            "ORG": "ORGANIZATION"
        }

        #pass entities from model to parent class
        super().__init__(
            supported_entities=list(self.label2presidio.values()),
            supported_language=supported_language
        )

    '''
    '''
    def load(self):
        ''' no loading is required '''
        pass

    '''
    '''
    def analyze(
        self,
        text,
        entities=None,
        nlp_artifacts=None
    ):
        predicted_entities = self.pipeline(text)

        results = [
            RecognizerResult(entity_type=self.label2presidio[e['entity_group']],
                             start=e['start'],
                             end=e['end'],
                             score=e['score']) for e in predicted_entities
        ]

        return results