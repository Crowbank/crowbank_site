from __future__ import unicode_literals
import json
from datetime import datetime

from django.db import models

# Create your models here.
STATUS_CHOICES = (
    ('', 'Just Created'),
    ('N', 'New and ready to be sent'),
    ('S', 'Sent but not confirmed'),
    ('V', 'Verified receipt'),
    ('C', 'Cancelled'),
    ('F', 'Failed'),
)


def message_reflector_handler(msg):
    pass


HANDLERS = {
    'deposit-request': None,
    'message-reflector': message_reflector_handler
}


class MessageQueue(models.Manager):
    def get_queryset(self):
        return super(MessageQueue, self).get_queryset().filter(status='N')

    def next(self):
        q = self.get_queryset()
        return q.earliest()


class Message(models.Model):
    no = models.AutoField(primary_key=True)
    thread = models.IntegerField(null=True)
    reply_to = models.IntegerField(null=True)
    type = models.CharField(max_length=100)
    payload = models.TextField()
    create_timestamp = models.DateTimeField(default=datetime.now)
    sent_timestamp = models.DateTimeField(null=True)
    confirmed_timestamp = models.DateTimeField(null=True)
    status = models.TextField(max_length=1, choices=STATUS_CHOICES, default='')
    reply_code = models.IntegerField(null=True)
    reply_message = models.CharField(max_length=200, default='')

    message_dict = {}
    queue = MessageQueue()
    objects = models.Manager()

    def __str__(self):
        return self.type

    def __getitem__(self, item):
        return self.message_dict[item]

    def __setitem__(self, key, value):
        self.message_dict[key] = value

    def __delitem__(self, key):
        del self.message_dict[key]

    def __len__(self):
        return len(self.message_dict)

    def __iter__(self):
        return self.message_dict.__iter__()

    def __contains__(self, item):
        return self.message_dict.__contains__(item)

    def send(self):
        self.status = 'N'
        self.save()

    def save(self, *args, **kwargs):
        if self.status == '':
            self.status = 'N'

        self.payload = json.dumps(self.message_dict)

        super(Message, self).save(*args, **kwargs)
        if not self.thread:
            self.thread = self.no
            super(Message, self).save(*args, **kwargs)

    def reply_message(self):
        reply = Message('reply-message')
        reply.thread = self.thread
        reply.reply_to = self.no

        return reply

    def unpack(self):
        self.message_dict = json.loads(self.payload)

    def set_reply(self, code):
        if code:
            self.reply_code = code
            self.status = 'V'
        else:
            self.reply_code = 0
            self.status = 'F'
        self.confirmed_timestamp = datetime.now()
        self.save()

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super(Message, cls).from_db(db, field_names, values)
        instance.unpack()
        return instance

    class Meta:
        get_latest_by = 'create_timestamp'
        ordering = ['create_timestamp']
