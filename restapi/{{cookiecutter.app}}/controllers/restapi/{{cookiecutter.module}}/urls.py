from django.urls import path
from {{cookiecutter.project_slug}}.urls import (
    URL_READ_ONLY,
    URL_DETAIL,
    URL_CREATE,
    URL_UPDATE,
    URL_DELETE
)

from .api import(
    ApiPublic{{cookiecutter.model}}ListDetail,
    ApiPrivate{{cookiecutter.model}}ViewSet
)

VERSION = 'v1'

urlpatterns = [
    # public
    path(
        f'{VERSION}/public/list',
        ApiPublic{{cookiecutter.model}}ListDetail.as_view(URL_READ_ONLY),
        name='api_public_{{cookiecutter.module}}_list_detail'
    ),

    # private
    path(
        f'{VERSION}/private/list',
        ApiPrivate{{cookiecutter.model}}ViewSet.as_view(URL_READ_ONLY),
        name='api_private_{{cookiecutter.module}}_list_detail'
    ),
    path(
        f'{VERSION}/private/create',
        ApiPrivate{{cookiecutter.model}}ViewSet.as_view(URL_CREATE),
        name='api_private_{{cookiecutter.module}}_create'
    ),
    path(
        f'{VERSION}/private/<pk>/update',
        ApiPrivate{{cookiecutter.model}}ViewSet.as_view(URL_UPDATE),
        name='api_private_{{cookiecutter.module}}_update'
    ),
    path(
        f'{VERSION}/private/<pk>/delete',
        ApiPrivate{{cookiecutter.model}}ViewSet.as_view(URL_DELETE),
        name='api_private_{{cookiecutter.module}}_delete'
    ),
]

"""
Add to urls.py urlpatterns:
    path('{{cookiecutter.module}}/api/', include('{{cookiecutter.app}}.controllers.restapi.{{cookiecutter.module}}.urls'))
"""