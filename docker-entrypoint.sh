#!/bin/bash
set -e

poetry run gunicorn --bind 0.0.0.0:$PORT todo_app.wsgi:app
