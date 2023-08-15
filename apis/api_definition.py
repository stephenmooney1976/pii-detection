#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 14:42:44 2023

@author: Stephen Mooney
"""

import flask

from http import HTTPStatus

from .anonymizer_class import AnonymizerClass

"""
"""

OK_STATUS_CODE = HTTPStatus.OK.value

class PersonalInfoAnonymizerAPI(object):

  """
  """
  def __init__(self):
    self.anonymizer_class = AnonymizerClass()


  """
  """
  def swaggerRedirect(self):
    return flask.redirect(f'{flask.request.url}ui')

  """
  """
  def singleAnonymizePII(self, body):
    input_text = body['inputText']
    output_text = self.anonymizer_class.anonymizeText(input_text)
    body['outputText'] = output_text

    return body

  """
  """
  def multiAnonymizePII(self, body):
    input_records = body['records']

    output_records = [dict(recordId=x['recordId'], inputText=x['inputText'], outputText=self.anonymizer_class.anonymizeText(x['inputText']))
      for x in input_records
    ]

    return output_records

  """
  """
  def readyState(self):
    return OK_STATUS_CODE

  """
  """
  def healthState(self):
    return OK_STATUS_CODE

"""
"""
class_instance = PersonalInfoAnonymizerAPI()