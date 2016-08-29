from django.shortcuts import render
from django.http import HttpResponse
import re
from datetime import date, timedelta
from petadmin_models.models import *
# Create your views here.


def index(request):
    return HttpResponse("Hello, world. Welcome to Crowbank's intranet.")

WEEKDAYS = {
    'mo': 0,
    'tu': 1,
    'we': 2,
    'th': 3,
    'fr': 4,
    'sa': 5,
    'su': 6
}


def decode_date(arg, base=None):
    if not base:
        base = date.today()

    longdate = re.compile('20(?P<year>1\d)(?P<month>\d\d)(?P<day>\d\d)')
    shortdate = re.compile('(?P<month>\d\d)(?P<day>\d\d)')
    weekday = re.compile('(?P<weekday>mo|tu|we|th|fr|sa|su)\w*', re.I)
    increment = re.compile('\+(?P<inc>\d+)')

    m = longdate.match(arg)
    if m:
        return date(int(m.group('year')), int(m.group('month')), int(m.group('day')))
    m = shortdate.match(arg)
    if m:
        base_date = date(base.year, int(m.group('month')), int(m.group('day')))
        if base_date < base:
            base_date = date(base.year + 1, int(m.group('month')), int(m.group('day')))
        return base_date

    m = weekday.match(arg)
    if m:
        base_wd = base.weekday()
        arg_wd = WEEKDAYS[m.group('weekday')]
        if arg_wd <= base_wd:
            arg_wd += 7
        return base + timedelta(arg_wd - base_wd)
    m = increment.match(arg)
    if m:
        return base + timedelta(int(m.group('inc')))
    return base


def date_dict_to_list(dict_form):
    list_form = []
    for (the_date, bookings) in dict_form.items():
        list_form.append({'date': the_date, 'bookings': bookings})
    return list_form


def inouts(request, io_args):
    split_args = io_args.split('/')
    from_date = decode_date(split_args[0])
    to_date = from_date

    if len(split_args) > 1:
        to_date = decode_date(split_args[1], from_date)

    additional_args = ''
    if len(split_args) > 2:
        additional_args = '/'.join(split_args[2:])

    dog_only_re = re.compile('.*dog.*', re.I)
    cat_only_re = re.compile('.*cat.*', re.I)

    no_dogs = dog_only_re.match(additional_args) is None
    no_cats = cat_only_re.match(additional_args) is None

    if no_cats and no_dogs:
        no_cats = False
        no_dogs = False

    ins = Booking.objects.filter(start_date__gte=from_date).filter(start_date__lte=to_date).exclude(status='N').exclude(status='C')
    outs = Booking.objects.filter(end_date__gte=from_date).filter(end_date__lte=to_date).exclude(status='N').exclude(status='C')

    ins_dog_dict = {}
    outs_dog_dict = {}
    ins_cat_dict = {}
    outs_cat_dict = {}

    for booking in ins:
        if booking.has_dogs():
            if booking.start_date in ins_dog_dict:
                ins_dog_dict[booking.start_date].append(booking)
            else:
                ins_dog_dict[booking.start_date] = [booking]
        if booking.has_cats():
            if booking.start_date in ins_cat_dict:
                ins_cat_dict[booking.start_date].append(booking)
            else:
                ins_cat_dict[booking.start_date] = [booking]

    ins_dog_list = date_dict_to_list(ins_dog_dict)
    ins_cat_list = date_dict_to_list(ins_cat_dict)

    for booking in outs:
        if booking.has_dogs():
            if booking.end_date in outs_dog_dict:
                outs_dog_dict[booking.end_date].append(booking)
            else:
                outs_dog_dict[booking.end_date] = [booking]
        if booking.has_cats():
            if booking.end_date in outs_cat_dict:
                outs_cat_dict[booking.end_date].append(booking)
            else:
                outs_cat_dict[booking.end_date] = [booking]

    outs_dog_list = date_dict_to_list(outs_dog_dict)
    outs_cat_list = date_dict_to_list(outs_cat_dict)

    if (not ins_dog_dict) and (not outs_dog_dict):
        no_dogs = True

    if (not ins_cat_dict) and (not outs_cat_dict):
        no_cats = True

    context = {'dog_ins': ins_dog_list,
               'dog_outs': outs_dog_list,
               'cat_ins': ins_cat_list,
               'cat_outs': outs_cat_list,
               'do_dogs': not no_dogs,
               'do_cats': not no_cats
               }

    return render(request, 'inouts.html', context)