from django import forms

from profiles.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'first_name',
            'middle_name',
            'last_name',
            'date_of_birth',
            'gender',
        )

    class Media:
        js = ('common/js/gijgo.min.js',)
        css = {
            'all': ('common/css/gijgo.min.css',)
        }