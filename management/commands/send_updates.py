from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import reverse

from django.db.models.query import Q

import datetime
from django.utils.timezone import utc
from django.core.mail import send_mail

import urllib2
import json

from orbut_backend.models import *

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

plaintext = get_template('email.txt')
h = get_template('email.html')

class Command(BaseCommand):
    help = 'sends an email users that have new items'

    def handle(self, *args, **options):
        today = datetime.datetime.utcnow().replace(tzinfo=utc)
        yesterday = today - datetime.timedelta(days=1)
        last_week = today - datetime.timedelta(days=7)
        last_month = today - datetime.timedelta(days=30)
        
        jobs = Job.objects.filter(Q(frequency=1) | Q(frequency=2, date__lte=last_week) | Q(frequency=3, date__lte=last_month))
        #jobs = Job.objects.all()
        for j in jobs:
            handle_query(j)
        
def handle_query(job):
    url = "http://api.dp.la/v1/items?" + job.q + "&sort_by=created&sort_order=desc&page_size=4"
    r = json.loads(urllib2.urlopen(url).read())
    items = []    
    for item in r['docs']:
        if not item['_id'] == job.last_item:
            items.append(item['_id'])
        else:
            break

    if len(items) > 0:
        job.last_item = items[0]
        job.save()

        d = Context({'items': items})
        text_content = plaintext.render(d)
        html_content = h.render(d)
        subject, from_email, to = "Follow That Cab Update", "example@dp.la", job.user.email

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    else:
        # update the date so we don't run this guy again until the next time
        job.save()
