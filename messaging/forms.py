from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from .models import Message, STATUS_CHOICES


class MessageFieldForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    content = forms.CharField(max_length=999)


class MessageForm(forms.Form):
    message_type = forms.CharField(max_length=100, required=True)
