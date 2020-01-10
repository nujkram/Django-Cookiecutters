USERNAME_REGEX = "^[a-zA-Z0-9.-]*$"

SUPERADMIN = 'SU'
ADMIN = 'ADM'
USER = 'USR'

USER_TYPE_CHOICES = (
    (SUPERADMIN, 'Super Admin'),
    (ADMIN, 'Admin'),
    (USER, 'User'),
)

USER_DASHBOARD_ROOTS = {
    SUPERADMIN: 'kfaf455ol5y2z4r53u44orsoc9rrvhw1cwn3jxee',
    ADMIN: 'dashboard/admin',
    USER: '',
}