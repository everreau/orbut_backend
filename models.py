from django.db import models
from django.contrib.auth.models import User

import datetime
from django.utils.timezone import utc

services = ((0, 'email'),)
frequencies = ((1, 'daily'), (2, 'weekly'), (3, 'monthly'))

class Output(models.Model):
    user = models.ForeignKey(User)
    service = models.IntegerField(choices=services)
    def __unicode__(self):
        return unicode(self.user) + ": " + unicode(self.service)

class Job(models.Model):
    user = models.ForeignKey(User)
    frequency = models.IntegerField(choices=frequencies)
    date = models.DateField()
    services = models.ManyToManyField(Output)
    last_item = models.CharField(max_length=255, blank=True, null=True)
    q = models.CharField(max_length=255)
    def save(self, **kwargs):
        self.date = datetime.datetime.utcnow().replace(tzinfo=utc)
        super(Job, self).save()
    def __unicode__(self):
        return unicode(self.user) + ": " + frequencies[self.frequency][1] + " - " + self.q
