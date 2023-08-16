#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 14:53:18 2023

@author: Stephen Mooney
"""

import connexion
from flask_cors import CORS
from waitress import serve
from huggingface_hub import snapshot_download

repo_id = 'dslim/bert-base-NER'
model_id = repo_id.split('/')[-1]

snapshot_download(repo_id=repo_id, local_dir=model_id)

import spacy

try:
  nlp_lg = spacy.load("en_core_web_lg")
except ModuleNotFoundError:
  spacy.cli.download(model="en_core_web_lg")

"""
"""
if __name__ == '__main__':
  try:
    app = connexion.FlaskApp(__name__, specification_dir='apis/specification')
    app.add_api('api-definition.yml')

    CORS(app.app)

    serve(app, host='0.0.0.0', port=10995)

  except Exception as e:
    raise e
