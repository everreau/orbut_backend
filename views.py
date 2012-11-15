from models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.core.urlresolvers import reverse

from forms import *

from django.contrib.auth.models import User
from models import *

import json

def post_json(request):
    if request.method == 'GET':
        frequencies = {"daily": 0, "weekly": 1, "monthly": 2}
        p = json.loads(request.GET['json'])
        print p
        user, created = User.objects.get_or_create(username=p['user_id'])
        user.email = p['user_id']
        user.save()
        email, created = Output.objects.get_or_create(user=user, service=0)
        email.save()
        job = Job(user=user, frequency=frequencies[p['frequency']], q='&'.join(p['query']))
        job.save()
        return HttpResponseRedirect(reverse(success, kwargs={'pk': job.pk}))
    else:
        return HttpResponseBadRequest()

def add_job(request):
    if request.method == 'POST':
        job = Job()
        form = JobForm(request.POST, instance=job)
        if form.is_valid():            
            job = form.save()
            return HttpResponseRedirect(reverse(success, kwargs={'pk': job.pk}))
    else:
        form = JobForm()
    return render_to_response('form.html',
                              {'form': form},
                              context_instance=RequestContext(request))

def success(request, pk):
    return render_to_response('success.html',
                              {'job': get_object_or_404(Job, pk=pk)},                              
                              context_instance=RequestContext(request))
