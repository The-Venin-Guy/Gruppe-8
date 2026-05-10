#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python -m textblob.download_corpora
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate