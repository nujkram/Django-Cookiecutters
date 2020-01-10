from django.urls import path

from accounts.controllers.views import AccountLoginView, AccountLogoutView

urlpatterns = [
    path('login', AccountLoginView.as_view(), name='accounts_login'),
    path('logout', AccountLogoutView.as_view(), name='accounts_logout'),
]