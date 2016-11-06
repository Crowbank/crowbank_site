from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from petadmin.models import Booking, Confirmation
from django.core.validators import validate_email


STATUS_CHOICES = (
    ('', 'Provisional'),
    ('V', 'Confirmed'),
    ('C', 'Cancelled'),
)

ACTION_CHOICES = (
    'Populate',
    'Generate',
    'Send',
)


def booking_number_validator(value):
    if not Booking.objects.filter(no=value).exists():
         raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': value},
        )


class MultiEmailField(forms.Field):
    def to_python(self, value):
        """Normalize data to a list of strings."""
        # Return an empty list if no input was given.
        if not value:
            return []
        l = value.split(',')
        return map(lambda x: x.strip(), l)

    def validate(self, value):
        """Check if value consists only of valid emails."""
        # Use the parent's handling of required fields, etc.
        super(MultiEmailField, self).validate(value)
        for email in value:
            validate_email(email)


class EmailTestForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True)
    email_list = MultiEmailField()
    restart = forms.BooleanField(required=False)


class SendConfirmationForm(forms.Form):
    email_to = MultiEmailField(label='To', required=False)
    email_cc = MultiEmailField(label='Cc', required=False)
    email_bcc = MultiEmailField(label='Bcc', required=False)

    def __init__(self, email=None, *args, **kwargs):
        if email and isinstance(email, basestring):
            super(SendConfirmationForm, self).__init__(*args, **kwargs)
            self.fields['email_to'].initial = email
        else:
            super(SendConfirmationForm, self).__init__(email, *args, **kwargs)


class ConfirmationForm(forms.Form):
    bk_no = forms.IntegerField(label='Booking Number', validators=[booking_number_validator])
    deluxe = forms.BooleanField(label='Deluxe', required=False)
    amended = forms.BooleanField(label='Amended', required=False)
    status = forms.ChoiceField(label='Deposit Required', choices=STATUS_CHOICES, required=False)
    deposit = forms.DecimalField(label='Deposit Amount', required=False)
    additional_text = forms.CharField(label='Additional Text', widget=forms.Textarea, required=False)

    def __init__(self, conf=None, *args, **kwargs):
        if conf and isinstance(conf, Confirmation):
            super(ConfirmationForm, self).__init__(*args, **kwargs)

            if conf:
                self.fields['bk_no'].initial = conf.booking.no
                self.fields['deluxe'].initial = conf.deluxe
                self.fields['amended'].initial = conf.amended
                if conf.cancelled:
                    self.fields['status'].initial = 'C'
                elif conf.deposit:
                    self.fields['status'].initial = ''
                    self.fields['deposit'].initial = conf.deposit_amount
                else:
                    self.fields['status'].initial = 'V'
        else:
            super(ConfirmationForm, self).__init__(conf, *args, **kwargs)


class InOutForm(forms.Form):
    PET_TYPES = (
        ('dog', 'Dogs Only'),
        ('cat', 'Cats Only'),
        ('both', 'Both Dogs and Cats'),
    )

    INOUT_TYPES = (
        ('in', 'Incoming Only'),
        ('out', 'Outgoing Only'),
        ('both', 'Both Incomings and Outgoings'),
    )

    from_date = forms.CharField(label='From Date', required=False, help_text="Use yymmdd or +n for n days from today, or ddd for weekday. Leave empty for today.")
    to_date = forms.CharField(label='To Date', required=False, help_text="Use yymmdd or +n for n days from start date, or ddd for weekday. Leave empty for start date.")
    pet_types = forms.ChoiceField(label='With Pets', choices=PET_TYPES, initial='both')
    in_or_out = forms.ChoiceField(label='Ins or Outs', choices=INOUT_TYPES, initial='both')
