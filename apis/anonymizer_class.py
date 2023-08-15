#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 15:31:31 2023

@author: Stephen Mooney
"""

from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

from .entity_recognizers import TransformerRecognizer

"""
"""
class AnonymizerClass(object):

  """
  """
  operators = {
      "DEFAULT": OperatorConfig("replace", {"new_value": "<ANONYMIZED>"}),
      "PHONE_NUMBER": OperatorConfig(
          "mask",
          {
              "type": "mask",
              "masking_char": "*",
              "chars_to_mask": 12,
              "from_end": True,
          },
      ),
      "US_SSN": OperatorConfig(
          "mask",
          {
              "type": "mask",
              "masking_char": "#",
              "chars_to_mask": 11,
              "from_end": False
          }
      ),
      "TITLE": OperatorConfig("redact", {}),
  }

  """
  """
  def __init__(self, model_dir='bert-base-NER'):
    __xfmr_recognizer = TransformerRecognizer(model_dir)
    self.analyzer = AnalyzerEngine()
    self.analyzer.registry.add_recognizer(__xfmr_recognizer)
    self.anonymizer_engine = AnonymizerEngine()

  """
  """
  def anonymizeText(self, input_text):
    __analyzer_results = self.analyzer.analyze(text=input_text, language='en')
    __anonymized_text = self.anonymizer_engine.anonymize(text=input_text,
                                                         analyzer_results=__analyzer_results,
                                                         operators=self.operators).text

    return __anonymized_text