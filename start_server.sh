#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

# Run the Uvicorn server
uvicorn app:app --host 0.0.0.0 --port 8000
