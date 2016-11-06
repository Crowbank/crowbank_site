from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from datetime import datetime
import json
from .models import Message, HANDLERS
from .forms import MessageFieldForm, MessageForm
from django.forms.formsets import formset_factory


# Create your views here.
@csrf_exempt
def dispatch(request):
    if request.method == 'POST' and request.POST and 'message' in request.POST:
        incoming_message = json.loads(request.POST['message'])
        if incoming_message:
            try:
                no = incoming_message['no']
                code = incoming_message['code']
                msg = incoming_message['msg']
                replied_message = Message.objects.filter(pk=no)[0]
                replied_message.set_reply(code)
                message_type = replied_message.type
                if type in HANDLERS and HANDLERS[type]:
                    HANDLERS[message_type](replied_message)
            except:
                return HttpResponse('Unrecognized incoming message')

    queue_length = Message.queue.count() - 1
    if queue_length >= 0:
        message = Message.queue.next()
        message.sent_timestamp = datetime.now()
        message.status = 'S'
        message.save()
        return HttpResponse(json.dumps({'no': message.no, 'type': message.type, 'payload': message.payload,
                                        'queue_length': queue_length}))
    else:
        return HttpResponse('')


def recent(request, n=10):
    messages = Message.objects.order_by('-create_timestamp')[:n]
    return render(request, 'messaging/recent.html', {'msgs': messages})


def inject(request):
    FieldFormSet = formset_factory(MessageFieldForm)
    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        field_formset = FieldFormSet(request.POST)
        if message_form.is_valid() and field_formset.is_valid():
            message_type = message_form.cleaned_data['message_type']
            message = Message(type=message_type)
            for field_form in field_formset:
                name = field_form.cleaned_data['name']
                content = field_form.cleaned_data['content']
                message[name] = content
            message.send()
            return HttpResponse('Successfully marked message #%d for sending' % message.no)
        else:
            return HttpResponse('Failed')
    else:
        message_form = MessageForm()
        field_formset = FieldFormSet()

    context = {
        'message_form': message_form,
        'field_formset': field_formset
    }

    return render(request, 'messaging/inject.html', context)
