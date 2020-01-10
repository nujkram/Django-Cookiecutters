from os import path
from split_settings.tools import optional, include

if path.isfile('/{{ cookiecutter.project_slug }}/local'):
    env = 'local'
elif path.isfile('/{{ cookiecutter.project_slug }}/onprem'):
    env = 'onprem'
elif path.isfile('/{{ cookiecutter.project_slug }}/staging'):
    env = 'staging'
else:
    env = 'prod'

include('apps.py')

include(f'environments/{env}.py')
