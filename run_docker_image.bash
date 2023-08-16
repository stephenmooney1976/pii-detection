#!/usr/bin/env bash

L_TAG=pii-container

docker build -t ${L_TAG} .

docker run -p 10995:10995 --rm ${L_TAG}
