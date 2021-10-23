from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NewUserForm(UserCreationForm):
    """ Extending the User Creation form base from Django
    See https://docs.djangoproject.com/en/1.8/_modules/django/contrib/auth/forms/#UserCreationForm
    and https://docs.djangoproject.com/en/3.2/topics/auth/default/#django.contrib.auth.forms.UserCreationForm
    """
    email = forms.EmailField(max_length=254,required=True, help_text="Please provide a valid email address we can use to contact you.")
    first_name = forms.CharField(max_length=150, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=150, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "first_name", "last_name")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user