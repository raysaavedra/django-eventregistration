from django.template import Context
from django.template.loader import get_template
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from profiles import models
from profiles import forms
from django.utils import simplejson
import datetime
from auth.views import admin_required

@admin_required
def create_account(request):
    context = {}
    context['success'] = False
    if request.method == 'POST':
        form1 = forms.UserCreationForm(request.POST)
        form2 = forms.NewUserForm(request.POST)

        if form1.is_valid() and form2.is_valid():
            profile = form2.save(commit=False)
            user = form1.save(commit=False)
            profile.username = user.username
            profile.password = user.password
            profile.save()
            context['success'] = True
            context['user_form'] = forms.NewUserForm()
            context['password_form'] = forms.UserCreationForm()
        else:
            context['password_form'] = form1
            context['user_form'] = form2
    else:
        context['user_form'] = forms.NewUserForm()
        context['password_form'] = forms.UserCreationForm()

    return render_to_response('profiles/create_account.html',context,context_instance=RequestContext(request))

@admin_required
def event(request):
    context = {}
    eventlist = models.EventList.objects.all()
    context['events'] = eventlist

    return render_to_response('profiles/event.html',context,context_instance=RequestContext(request))


@admin_required
def create_event(request):
    context = {}
    context['success'] = False

    if request.method == 'POST':
        form1 = forms.EventForm(request.POST)
        if form1.is_valid():
            f1 = form1.save()
            newuser = models.NewUser.objects.get(id=request.user.id)
            eventlist = models.EventList.objects.create(account=newuser,event=f1,activated=False)
            context['success'] = True
            context['eventform'] = forms.EventForm()
        else:
            context['eventform'] = form1
    else:
        context['eventform'] = forms.EventForm()

    return render_to_response('profiles/create_event.html',context,context_instance=RequestContext(request))

@admin_required
def activate_event(request):
    if request.is_ajax():
        eventid = request.GET.get('q')
        if eventid is not None:
            try:
                activated_event = models.EventList.objects.get(activated=True)
                activated_event.activated = False
                activated_event.save()
            except:
                print 'no events activated'

            newevent = models.EventList.objects.get(pk=eventid)
            newevent.activated = True
            newevent.save()

            request.session['event_activated'] = newevent.event.name
            request.session['event_id'] = newevent.id
            data = simplejson.dumps(newevent.event.name)
            return HttpResponse(data, mimetype='application/javascript')

@admin_required
def deactivate_event(request):
    if request.is_ajax():
        newuser = models.NewUser.objects.get(id=request.user.id)
        eventlist = EventList.objects.get(account=newuser,activated=True)
        eventlist.activated=False
        eventlist.save()

        del request.session['event_activated']
        del request.session['event_id']
        data = simplejson.dumps(eventlist.event.name)
        return HttpResponse(data, mimetype='application/javascript')


@admin_required
def add_student(request):
    context = {}
    context['success'] = False

    if request.method == 'POST':
        form1 = forms.StudentForm(request.POST)
        if form1.is_valid():
            f1 = form1.save()
            context['success'] = True
            context['studentform'] = forms.StudentForm()
        else:
            context['studentform'] = form1
    else:
        context['studentform'] = forms.StudentForm()

    return render_to_response('profiles/add_student.html',context,context_instance=RequestContext(request))
