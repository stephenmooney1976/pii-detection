#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 12:20:38 2023

@author: Stephen Mooney
"""

from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer import AnalyzerEngine
from typing import List

from presidio_analyzer import AnalyzerEngine, EntityRecognizer, RecognizerResult
from presidio_analyzer.nlp_engine import NlpArtifacts
from transformers import pipeline

# load spacy model -> workaround
import os
os.system("spacy download en_core_web_lg")

# list of entities: https://microsoft.github.io/presidio/supported_entities/#list-of-supported-entities
DEFAULT_ANOYNM_ENTITIES = [
    "CREDIT_CARD",
    "CRYPTO",
    "DATE_TIME",
    "EMAIL_ADDRESS",
    "IBAN_CODE",
    "IP_ADDRESS",
    "NRP",
    "LOCATION",
    "PERSON",
    "PHONE_NUMBER",
    "MEDICAL_LICENSE",
    "URL",
    "ORGANIZATION"
]

# init anonymize engine
engine = AnonymizerEngine()