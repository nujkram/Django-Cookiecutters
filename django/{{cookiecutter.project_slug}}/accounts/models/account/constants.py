import os
import random
import string

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USERNAME_REGEX = "^[a-zA-Z0-9.-]*$"

try:
    with open(os.path.join(BASE_DIR, 'ADMIN_URL')) as f:
        ADMIN_URL = f.read().strip()
except FileNotFoundError:
    generated_key = ''.join([random.SystemRandom().choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(50)])
    secret = open(os.path.join(BASE_DIR, 'ADMIN_URL'), 'w')
    secret.write(generated_key)
    secret.close()
    ADMIN_URL = generated_key

SUPERADMIN = 'SU'
ADMIN = 'ADM'
USER = 'USR'

USER_TYPE_CHOICES = (
    (SUPERADMIN, 'Super Admin'),
    (ADMIN, 'Admin'),
    (USER, 'User'),
)

USER_DASHBOARD_ROOTS = {
    SUPERADMIN: ADMIN_URL,
    ADMIN: 'dashboard/admin',
    USER: '',
}