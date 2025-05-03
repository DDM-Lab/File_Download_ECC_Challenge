#!/bin/bash

set -e

socat tcp-listen:5555,reuseaddr,fork EXEC:"python3 /app/main.py --control"
