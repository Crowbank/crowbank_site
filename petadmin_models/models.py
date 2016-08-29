# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class HistoryStore(models.Model):
    timemark = models.DateTimeField()
    table_name = models.TextField()
    pk_date_src = models.TextField()
    pk_date_dest = models.TextField()
    record_state = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'history_store'
        unique_together = (('table_name', 'pk_date_dest'),)


SEX_CHOICES = (
    ('Dog', 'Dog'),
    ('Cat', 'Cat'),
)

class Customer(models.Model):
    no = models.AutoField(primary_key=True, db_column='cust_no')
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

    class Meta:
        managed = False
        db_table = 'tblcustomer'

    def __str__(self):
        return self.surname

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
    spec = models.CharField(max_length=3, db_column='breed_spec', choices=SEX_CHOICES)
    desc = models.CharField(max_length=35, db_column='breed_desc')

    class Meta:
        managed = False
        db_table = 'tblbreed'

    def __str__(self):
        return self.desc


class Pet(models.Model):
    no = models.AutoField(primary_key=True, db_column='pet_no')
    cust = models.ForeignKey(Customer, db_column='pet_cust_no')
    name = models.CharField(max_length=20, db_column='pet_name')
    spec = models.CharField(max_length=3, db_column='pet_spec')
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
    no = models.AutoField(primary_key=True, db_column='bk_no')
    cust = models.ForeignKey(Customer, db_column='bk_cust_no')
    start_date = models.DateTimeField(blank=True, null=True, db_column='bk_start_date')
    end_date = models.DateTimeField(blank=True, null=True, db_column='bk_end_date')
    start_time = models.CharField(max_length=10, db_column='bk_start_time')
    end_time = models.CharField(max_length=10, db_column='bk_end_time')
    gross_amt = models.FloatField(db_column='bk_gross_amt')
    paid_amt = models.FloatField(db_column='bk_paid_amt')
    amt_outstanding = models.FloatField(db_column='bk_amt_outstanding')
    status = models.CharField(max_length=1, db_column='bk_status')
    create_date = models.DateTimeField(blank=True, null=True, db_column='bk_create_date')
    pets = models.ManyToManyField(Pet, through='BookingItem', through_fields=('bk', 'pet'))

    class Meta:
        managed = False
        db_table = 'tblbooking'

    def __str__(self):
        return 'bk #%d' % self.no

    def has_cats(self):
        for pet in self.pets.all():
            if pet.spec == 'Cat':
                return True
        return False

    def has_dogs(self):
        for pet in self.pets.all():
            if pet.spec == 'Dog':
                return True
        return False


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
