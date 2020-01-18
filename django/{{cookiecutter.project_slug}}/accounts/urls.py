from django.urls import path

from controllers.views.account import main as account_views
from controllers.restapi.account import main as account_api

urlpatterns = [
    path('login', account_views.AccountLoginView.as_view(), name='accounts_login'),
    path('logout', account_views.AccountLogoutView.as_view(), name='accounts_logout'),
]

################################################################################
# API
################################################################################
urlpatterns += [
    path('api/v1/login', account_api.ApiLoginWithCredentials.as_view(), name='api_accounts_login'),
    path('api/v1/register', account_api.ApiPublicAccountCreate.as_view(), name='api_accounts_register')
]