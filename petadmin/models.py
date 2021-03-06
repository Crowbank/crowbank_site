# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
import decimal
import urllib2
import datetime
from django.template import loader
from django.core.mail import EmailMessage
from messaging.models import Message
import logging

logger = logging.getLogger('crowbank')


SEX_CHOICES = (
    ('Dog', 'Dog'),
    ('Cat', 'Cat'),
)


class Customer(models.Model):
    no = models.AutoField(primary_key=True, db_column='cust_no')
    title = models.CharField(max_length=10, db_column='cust_title')
    surname = models.CharField(max_length=30, db_column='cust_surname')
    forename = models.CharField(max_length=30, db_column='cust_forename')
    addr1 = models.CharField(max_length=50, db_column='cust_addr1')
    addr2 = models.CharField(max_length=50, db_column='cust_addr2')
    addr3 = models.CharField(max_length=50, db_column='cust_addr3')
    postcode = models.CharField(max_length=15, db_column='cust_postcode')
    telno_home = models.CharField(max_length=20, db_column='cust_telno_home')
    email = models.CharField(max_length=255, db_column='cust_email')
    telno_mobile = models.CharField(max_length=20, db_column='cust_telno_mobile')
    telno_mobile2 = models.CharField(max_length=20, db_column='cust_telno_mobile2')
    nodeposit = models.IntegerField(db_column='cust_nodeposit')
    deposit_requested = models.IntegerField(db_column='cust_deposit_requested')

    class Meta:
        managed = False
        db_table = 'tblcustomer'

    def __str__(self):
        return self.surname

    @property
    def display_name(self):
        if self.title == '':
            display_name = ''
        else:
            display_name = self.title + ' '

        if self.forename != '':
            display_name += ' ' + self.forename

        if display_name != '':
            display_name += ' '

        display_name += self.surname

        return display_name


class Vet(models.Model):
    no = models.AutoField(primary_key=True, db_column='vet_no')
    practice_name = models.CharField(max_length=50, db_column='vet_practice_name')
    addr1 = models.CharField(max_length=50, db_column='vet_addr1')
    addr2 = models.CharField(max_length=50, db_column='vet_addr2')
    addr3 = models.CharField(max_length=50, db_column='vet_addr3')
    postcode = models.CharField(max_length=15, db_column='vet_postcode')
    telno_1 = models.CharField(max_length=20, db_column='vet_telno_1')
    email = models.CharField(max_length=50, db_column='vet_email')
    website = models.CharField(max_length=50, db_column='vet_website')

    class Meta:
        managed = False
        db_table = 'tblvet'

    def __str__(self):
        return self.practice_name


class Breed(models.Model):
    no = models.AutoField(primary_key=True, db_column='breed_no')
    species = models.CharField(max_length=3, db_column='breed_spec', choices=SEX_CHOICES)
    desc = models.CharField(max_length=35, db_column='breed_desc')

    class Meta:
        managed = False
        db_table = 'tblbreed'

    def __str__(self):
        return self.desc


class Pet(models.Model):
    SPEC_CHOICES = ('Dog', 'Cat',)
    
    no = models.AutoField(primary_key=True, db_column='pet_no')
    customer = models.ForeignKey(Customer, db_column='pet_cust_no')
    name = models.CharField(max_length=20, db_column='pet_name')
    species = models.CharField(max_length=3, db_column='pet_spec')
    breed = models.ForeignKey(Breed, db_column='pet_breed_no')
    dob = models.DateTimeField(blank=True, null=True, db_column='pet_dob')
    sex = models.CharField(max_length=1, db_column='pet_sex', choices=SEX_CHOICES)
    vet = models.ForeignKey(Vet, db_column='pet_vet_no')

    class Meta:
        managed = False
        db_table = 'tblpet'

    def __str__(self):
        return '%s (%s)' % (self.name, self.breed.desc)


class Booking(models.Model):
    STATUS_CHOICES = (
        ('P', 'Provisional'),
        ('V', 'Confirmed'),
        ('C', 'Cancelled'),
        ('N', 'No Show'),
    )

    no = models.AutoField(primary_key=True, db_column='bk_no')
    customer = models.ForeignKey(Customer, db_column='bk_cust_no')
    start_date = models.DateField(blank=True, null=True, db_column='bk_start_date')
    end_date = models.DateField(blank=True, null=True, db_column='bk_end_date')
    start_datetime = models.DateTimeField(blank=True, null=True, db_column='bk_start_datetime')
    end_datetime = models.DateTimeField(blank=True, null=True, db_column='bk_end_datetime')
    start_time = models.CharField(max_length=10, db_column='bk_start_time')
    end_time = models.CharField(max_length=10, db_column='bk_end_time')
    gross_amt = models.FloatField(db_column='bk_gross_amt')
    paid_amt = models.FloatField(db_column='bk_paid_amt')
    amt_outstanding = models.FloatField(db_column='bk_amt_outstanding')
    status = models.CharField(max_length=1, db_column='bk_status', choices=STATUS_CHOICES)
    peak = models.IntegerField(db_column='bk_peak')
    skip_confirmation = models.IntegerField(db_column='bk_skip_confirmation')
    deluxe = models.IntegerField(db_column='bk_deluxe')
    create_date = models.DateTimeField(blank=True, null=True, db_column='bk_create_date')
    pets = models.ManyToManyField(Pet, through='BookingItem', through_fields=('bk', 'pet'))

    class Meta:
        managed = False
        db_table = 'tblbooking'

    def __str__(self):
        return 'bk #%d' % self.no

    def has_cats(self):
        for pet in self.pets.all():
            if pet.species == 'Cat':
                return True
        return False

    def has_dogs(self):
        for pet in self.pets.all():
            if pet.species == 'Dog':
                return True
        return False

    def pet_names(self):
        pets = list(self.pets.all())
        if len(pets) == 1:
            return pets[0].name
        return ', '.join(map(lambda p: p.name, pets[0:-1])) + ' and ' + pets[-1].name


class ReportParameters:
    def __init__(self):
        self.report = "intranet/Confirmation.html"
        self.logo_file = "/static/img/Logo.jpg"
        self.deluxe_logo_file = "/static/img/deluxe_logo_2.png"
        self.pay_deposit_file = "/static/img/paydeposit.png"
        self.logo_code = None
        self.deluxe_logo_code = None
        self.deposit_icon = None
        self.past_messages = []

    def read_images(self):
        with open(self.logo_file, "rb") as f:
            data = f.read()
            self.logo_code = data.encode("base64")

        with open(self.deluxe_logo_file, "rb") as f:
            data = f.read()
            self.deluxe_logo_code = data.encode("base64")

        with open(self.pay_deposit_file, "rb") as f:
            data = f.read()
            self.deposit_icon = data.encode("base64")


class Confirmation:
    @staticmethod
    def get_deposit_url(bk_no, deposit_amount, pet_names, customer):
        url = "https://secure.worldpay.com/wcc/purchase?instId=1094566&cartId=PBL-%d&amount=%f&currency=GBP&" %\
              (bk_no, deposit_amount)
        url += 'desc=Deposit+for+Crowbank+booking+%%23%d+for+%s&accId1=CROWBANKPETBM1&testMode=0' % (bk_no, pet_names)
        url += '&name=%s' % urllib2.quote(customer.display_name)
        if customer.email != '':
            url += '&email=%s' % urllib2.quote(customer.email)
        if customer.addr1 != '':
            url += '&address1=%s' % urllib2.quote(customer.addr1)
        if customer.addr2 != '':
            url += '&address2=%s' % urllib2.quote(customer.addr2)
        if customer.addr3 != '':
            url += '&town=%s' % urllib2.quote(customer.addr3)
        if customer.postcode != '':
            url += '&postcode=%s' % urllib2.quote(customer.postcode)
        url += '&country=UK'
        if customer.telno_home != '':
            phone = customer.telno_home
            if len(phone) == 6:
                phone = '01236 ' + phone
            url += '&tel=%s' % urllib2.quote(phone)

        return url

    def __init__(self, booking):
        self.booking = booking
        self.amended = False
        self.new = False        # a new booking - any subsequent amendments are 'swallowed'
        self.payment = False    # flag determining whether a payment is acknowledged
        self.amended = False    # flag determining whether this is an amendment of an existing booking
        self.deposit = True     # flag determining whether a deposit request is necessary
        self.deposit_amount = None
        self.conf_no = 0
        self.payment_amount = decimal.Decimal("0.00")
        self.payment_date = None
        self.title = ''
        self.cancelled = self.booking.status == 'C'
        self.deluxe = (self.booking.deluxe == 1)
        self.booking_count = 0
        self.past_messages = []
        self.force_deposit = False
        self.skip = (self.booking.skip_confirmation == 1)
        self.in_2017 = False
        self.deposit_url = ''
        self.rationale = ''
        self.additional_text = ''
        self.email = ''
        self.subject = ''

        if self.booking.start_date.year > 2016:
            self.in_2017 = True

        if self.booking.deluxe == 1:
            self.deluxe = True

        self.evaluate_parameters()

    def evaluate_parameters(self):
        if self.booking.customer.email:
            self.email = self.booking.customer.email

        if self.force_deposit:
            self.deposit = True
        else:
            if self.in_2017:
                self.deposit = False
                self.rationale = '2017 Booking'

            if self.deposit and self.booking.status == 'V':
                self.deposit = False
                self.rationale = 'Confirmed Booking'

            if self.deposit and self.booking.paid_amt != decimal.Decimal("0.00"):
                self.deposit = False
                self.rationale = 'Deposit Paid'

            if self.deposit and self.booking.customer.nodeposit:
                self.deposit = False
                self.rationale = 'No-deposit Customer'

            if self.deposit and self.booking.peak == 0:
                self.deposit = False
                self.rationale = 'Off-peak Booking'

            if self.deposit and self.payment_amount != decimal.Decimal("0.00"):
                self.deposit = False
                self.rationale = 'Payment made'

            if self.deposit and self.booking.customer.deposit_requested:
                self.deposit = False
                self.rationale = 'Deposit already requested'

        if self.deposit and not self.deposit_amount:
            self.deposit_amount = self.calculate_deposit_amount()

            if self.deposit_amount == decimal.Decimal("0.00"):
                self.deposit_amount = decimal.Decimal("30.00")
                for pet in self.booking.pets.all():
                    if pet.species == 'Dog':
                        self.deposit_amount = decimal.Decimal("50.00")
                if self.deposit_amount > self.booking.gross_amt / 2:
                    self.deposit_amount = decimal.Decimal(self.booking.gross_amt) / 2

            self.deposit_url = Confirmation.get_deposit_url(self.booking.no, self.deposit_amount,
                                                            self.booking.pet_names(), self.booking.customer)

        if self.cancelled:
            self.title = 'Booking Cancellation'
        else:
            if self.deposit:
                if self.deluxe:
                    self.title = 'Provisional Deluxe Booking'
                else:
                    self.title = 'Provisional Booking'
            else:
                if self.deluxe:
                    self.title = 'Confirmed Deluxe Booking'
                else:
                    self.title = 'Confirmed Booking'

            if self.amended:
                self.title += ' - Amended'

        self.subject = '%s #%d' % (self.title, self.booking.no)

    def calculate_deposit_amount(self):
        deposit_amount = decimal.Decimal("30.00")
        for pet in self.booking.pets.all():
            if pet.species == 'Dog':
                deposit_amount = decimal.Decimal("50.00")
            if deposit_amount > self.booking.gross_amt / 2:
                deposit_amount = decimal.Decimal(self.booking.gross_amt) / 2
        return deposit_amount

    def body(self, report_parameters=None):
        today_date = datetime.date.today()

        template = loader.get_template('intranet/confirmation_body.html')

        self.evaluate_parameters()

        body = template.render({'today_date': today_date, 'conf': self})

        return body

    def send(self, email_to, email_cc=None, email_bcc=None, subject=None, body=None):
        if not subject:
            subject = '%s #%d' % (self.title, self.booking.no)

        if not body:
            body = self.body()

        email_msg = EmailMessage(subject, body, None, email_to, cc=email_cc, bcc=email_bcc)
        email_msg.content_subtype = 'html'
        email_msg.send()

        msg = Message(type='confirmation-sent')
        msg['bk_no'] = self.booking.no
        if self.deposit:
            msg['deposit_amount'] = self.deposit_amount

        msg['body'] = body

        now = datetime.datetime.now()
        file_name = "%d_%s.html" % (self.booking.no, now.strftime("%Y%m%d%H%M%S"))
        msg['file_name'] = file_name
        msg['subject'] = subject

        msg.send()


class BookingItem(models.Model):
    bk = models.ForeignKey(Booking, db_column='bi_bk_no')
    pet = models.ForeignKey(Pet, db_column='bi_pet_no')

    class Meta:
        managed = False
        db_table = 'tblbookingitem'
        unique_together = (('bk', 'pet'),)


class Payment(models.Model):
    PAY_CHOICES = (
        ('Debit Card', 'Card Machine'),
        ('Cash', 'Cash'),
        ('Credit Card', 'WorldPay Online'),
    )
    no = models.AutoField(primary_key=True, db_column='pay_no')
    bk = models.ForeignKey(Booking, db_column='pay_bk_no')
    cust = models.ForeignKey(Customer, db_column='pay_cust_no')
    date = models.DateTimeField(blank=True, null=True, db_column='pay_date')
    amount = models.FloatField(db_column='pay_amount')
    type = models.CharField(max_length=12, db_column='pay_type', choices=PAY_CHOICES)

    class Meta:
        managed = False
        db_table = 'tblpayment'

    def __str__(self):
        return 'Payment #%d' % self.no


class Employee(models.Model):
    RANK_CHOICES = (
        (1, 'Shift Leader'),
        (2, 'Kennel Assistant'),
        (3, 'Volunteer'),
    )
    no = models.AutoField(primary_key=True, db_column='emp_no')
    forename = models.CharField(max_length=30, db_column='emp_forename')
    surname = models.CharField(max_length=30, db_column='emp_surname')
    rank = models.IntegerField(choices=RANK_CHOICES)

    def __str__(self):
        return self.forename + ' ' + self.surname

    class Meta:
        db_table = 'tblemployee'


class MedicalCondition(models.Model):
    no = models.AutoField(primary_key=True, db_column='mc_no')
    desc = models.CharField(max_length=100, db_column='mc_desc')
    def __str__(self):
        return self.desc

    class Meta:
        db_table = 'tblmedicalcondition'


class VetVisit(models.Model):
    CHARGE_CHOICES = (
        ('P', 'Pending'),
        ('I', 'Invoiced'),
        ('C', 'Charged'),
        ('A', 'Absorbed'),
        ('S', 'Submitted to Insurer'),
        ('R', 'Repaid by Insurer'),
    )
    no = models.AutoField(primary_key=True, db_column='vv_no')
    bk = models.ForeignKey(Booking, db_column='vv_bk_no')
    pet = models.ForeignKey(Pet, db_column='vv_pet_no')
    vet = models.ForeignKey(Vet, db_column='vv_vet_no')
    visit_date = models.DateField(db_column='vv_date')
    amount = models.FloatField(db_column='vv_amount')
    status = models.CharField(max_length=1, db_column='vv_status', choices=CHARGE_CHOICES)
    med = models.ForeignKey(MedicalCondition, db_column='vv_mc_no')

    def __str__(self):
        return '%s (%s)' % (self.pet.name, self.visit_date.strftime("%d/%m/%y"))

    class Meta:
        db_table = 'tblvetvisit'
