#!/usr/bin/env bash

L_NUM_CONTAINERS=3

rpk container start -n ${L_NUM_CONTAINERS} | grep export | sed -e 's/^[ \t]*//' > redpanda.env

sleep 60

exit 0
