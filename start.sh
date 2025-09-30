#!/bin/bash
gunicorn app:app --bind 0.0.0.0:8000 &  # run gunicorn in background
python3 main.py     # run main.py in foreground
