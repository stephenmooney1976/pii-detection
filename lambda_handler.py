#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 14:53:18 2023

@author: Stephen Mooney
"""

import json
from apis.anonymizer_class import AnonymizerClass

anonymizer_class = AnonymizerClass()

def handler(event, context):
  input_text = event['inputText']
  output_text = anonymizer_class.anonymizeText(input_text)

  return {
    "statusCode": 200,
    "headers": {
      "Content-Type": "application/json"
    },
    "body": json.dumps({
      "outputText": output_text
    })
  }

