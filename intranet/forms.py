from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from petadmin_models.models import Booking, Confirmation


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


class BookingSelectionForm(forms.Form):
    bk_no = forms.IntegerField(label='Booking Number', validators=[booking_number_validator])


class SendConfirmationForm(forms.Form):
    email = forms.EmailField(label='Email Address', max_length=100, required=False)

    def __init__(self, conf=None, *args, **kwargs):
        if conf and isinstance(conf, Confirmation):
            super(SendConfirmationForm, self).__init__(*args, **kwargs)

            if conf:
                self.bk_no = conf.booking.no
                self.fields['email'].initial = conf.booking.customer.email


class ConfirmationOptionsForm(forms.Form):
    bk_no = 0
    deluxe = forms.BooleanField(label='Deluxe', required=False)
    amended = forms.BooleanField(label='Amended', required=False)
    status = forms.ChoiceField(label='Deposit Required', choices=STATUS_CHOICES, required=False)
    deposit = forms.DecimalField(label='Deposit Amount', required=False)
    additional_text = forms.CharField(label='Additional Text', widget=forms.Textarea, required=False)

    def __init__(self, conf=None, *args, **kwargs):
        if conf and isinstance(conf, Confirmation):
            super(ConfirmationOptionsForm, self).__init__(*args, **kwargs)

            if conf:
                self.bk_no = conf.booking.no
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


class ConfirmationForm(forms.Form):
    bk_no = forms.IntegerField(label='Booking Number', validators=[booking_number_validator])
    email = forms.EmailField(label='Email Address', max_length=100, required=False)
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
                self.fields['email'].initial = conf.booking.customer.email
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

    from_date = forms.CharField(label='From Date', required=False)
    to_date = forms.CharField(label='To Date', required=False)
    pet_types = forms.ChoiceField(label='With Pets', choices=PET_TYPES, initial='both')
    in_or_out = forms.ChoiceField(label='Ins or Outs', choices=INOUT_TYPES, initial='both')
