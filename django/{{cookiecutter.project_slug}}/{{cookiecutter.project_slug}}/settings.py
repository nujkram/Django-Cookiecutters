import os
from split_settings.tools import include

try:
    with open('{{ cookiecutter.project_slug }}/ENV') as f:
        ENV = f.read().strip()
except FileNotFoundError:
    ENV = 'prod'
    env_file = open('{{ cookiecutter.project_slug }}/ENV', 'w')
    env_file.write(ENV)
    env_file.close()

include('apps.py')
include(f'environments/{ENV}.py')
