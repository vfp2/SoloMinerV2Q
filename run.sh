#!/bin/bash
export $(grep -v '^#' .env | xargs)
python3.11 SoloMinerV2.py
