#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 14:53:18 2023

@author: Stephen Mooney
"""

import connexion
from flask_cors import CORS
from waitress import serve

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
