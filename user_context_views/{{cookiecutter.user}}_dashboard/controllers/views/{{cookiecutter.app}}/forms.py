from django import forms
from {{ cookiecutter.parent }}.models.{{ cookiecutter.app_singular }}.models import {{ cookiecutter.model }}

class {{ cookiecutter.model }}Form(forms.ModelForm):
    class Meta:
        model = {{ cookiecutter.model }}
        fields = '__all__'
