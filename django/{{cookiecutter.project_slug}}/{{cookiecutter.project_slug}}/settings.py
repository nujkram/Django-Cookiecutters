import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from split_settings.tools import include

try:
    with open(os.path.join(BASE_DIR, 'ENV')) as f:
        ENV = f.read().strip()
except FileNotFoundError:
    ENV = 'prod'
    env_file = open(os.path.join(BASE_DIR, 'ENV'), 'w')
    env_file.write(ENV)
    env_file.close()

include('apps.py')
include(f'environments/{ENV}.py')
