#!/bin/bash
celery -A {{ cookiecutter.project_slug }} worker --loglevel=debug --logfile=/{{ cookiecutter.project_slug }}/logs/celery.log
