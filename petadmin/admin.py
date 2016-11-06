from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import Employee, VetVisit, MedicalCondition

admin.site.register(Employee)
admin.site.register(MedicalCondition)
admin.site.register(VetVisit)
