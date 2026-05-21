#!/bin/bash

# 1. Install dependencies cleanly
pip install -r requirements.txt

# 2. Collect static files
python manage.py collectstatic --noinput

# 3. Apply your database migrations to Neon
python manage.py migrate