#!/usr/bin/env bash
coverage run manage.py test -v 2 --force-color
echo "Generating coverage report..."
coverage html
