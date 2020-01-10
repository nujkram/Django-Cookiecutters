from django.urls import path

from profiles.controllers.views import profile_views

urlpatterns = [
    path('', profile_views.ProfileHomeView.as_view(), name='profile_home_view'),
    path('update/', profile_views.ProfileUpdateView.as_view(), name='profile_update_view'),
    path('account/update/', profile_views.AccountUpdateView.as_view(), name='account_update_view'),
    path('account/password/', profile_views.AccountPasswordUpdateView.as_view(), name='account_password_view'),
]