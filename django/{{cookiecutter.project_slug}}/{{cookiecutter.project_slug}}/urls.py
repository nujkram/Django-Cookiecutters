"""servioPayroll URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from accounts.controllers.views.account.main import AccountLoginView 
from accounts.models.account.constants import ADMIN_URL

URL_READ_ONLY = {
    'get': 'list'
}

URL_DETAIL = {
    'get': 'retrieve'
}

URL_CREATE = {
    'get': 'list',
    'post': 'create',
}

URL_UPDATE = {
    'get': 'retrieve',
    'put': 'update',
    # 'patch': 'update_partial'
}

URL_DELETE = {
    'get': 'retrieve',
    'delete': 'destroy'
}

urlpatterns = [
    path('', AccountLoginView.as_view(), name='root'),
    path(ADMIN_URL, admin.site.urls),

    path('profile/', include('profiles.urls')),
    path('accounts/', include('accounts.urls')),


    # dashboards
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),

    ]
