#!/bin/bash
export $(grep -v '^#' .env | xargs)
python3 SoloMinerV2.py