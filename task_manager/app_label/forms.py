from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Label


class LabelCreationForm(forms.ModelForm):
    status_name = _("Name")
    name = forms.CharField(label=status_name, max_length=40, required=True)
    status_description = _("Description")
    description = forms.CharField(
        label=status_description,
        max_length=255,
        required=False
    )

    class Meta:
        model = Label
        fields = [
            'name',
            'description',
        ]
