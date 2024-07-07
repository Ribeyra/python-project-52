from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import User


class CustomUserCreationForm(UserCreationForm):
    first_name_label = _("First name")
    first_name = forms.CharField(
        label=first_name_label, max_length=30, required=True
    )
    last_name_label = _("Last name")
    last_name = forms.CharField(
        label=last_name_label, max_length=30, required=True
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2'
        ]


class CustomUserChangeForm(UserCreationForm):
    first_name_label = _("First name")
    first_name = forms.CharField(
        label=first_name_label, max_length=30, required=True
    )
    last_name_label = _("Last name")
    last_name = forms.CharField(
        label=last_name_label, max_length=30, required=True
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2'
        ]

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(
            pk=self.instance.pk
        ).filter(username=username).exists():
            raise forms.ValidationError('Username already exists.')
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password_label = _("Password")
    password = forms.CharField(
        label=password_label,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
