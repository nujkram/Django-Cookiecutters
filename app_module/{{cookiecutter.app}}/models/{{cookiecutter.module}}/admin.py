from django.contrib import admin

from .models import {{cookiecutter.model}}

class {{cookiecutter.model}}Admin(admin.ModelAdmin):
    list_display = ['id', 'created']
    list_filter = ['id']
    search_fields = ['id']
    ordering = ['-created']

admin.site.register({{cookiecutter.model}}, {{cookiecutter.model}}Admin)