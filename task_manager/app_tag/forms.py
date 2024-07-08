from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Tag


class TagCreationForm(forms.ModelForm):
    status_name = _("Tag name")
    name = forms.CharField(label=status_name, max_length=40, required=True)
    status_description = _("Tag description")
    description = forms.CharField(
        label=status_description,
        max_length=255,
        required=False
    )

    class Meta:
        model = Tag
        fields = [
            'name',
            'description',
        ]
