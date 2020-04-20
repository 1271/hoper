#!/usr/bin/env bash

if [[ 1 -le $(python util.py http://google.com -CFj) ]]
then
    exit 0
else
    exit 1
fi
