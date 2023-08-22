#!/usr/bin/env bash

L_TAG=pii-api-ontainer

docker build -t ${L_TAG} .

docker run -p 10995:10995 --rm ${L_TAG}

exit 0
