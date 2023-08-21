#!/usr/bin/env bash

docker-compose up -d

rpk topic delete random-pii-text
rpk topic delete random-pii-text-anon

rpk topic create random-pii-text -p 3
rpk topic create random-pii-text-anon -p 3
