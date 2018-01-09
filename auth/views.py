# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from profiles.models import NewUser,EventList
from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse

def login_user(request):
	username = password = ''
	context = {}
	context['check_errors']=False

	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				if user.username != 'admin':
					if user.newuser.usertype == 'a':
						request.session['isadmin'] = True
					else:
						request.session['isadmin'] = False
					try:
						eventlist = EventList.objects.get(activated=True)
						request.session['event_activated'] = eventlist.event.name
						request.session['event_id'] = eventlist.id
						return HttpResponseRedirect('/')
					except:
						return HttpResponseRedirect('/')
				else:
					request.session['isadmin'] = True
					try:
						eventlist = EventList.objects.get(activated=True)
						request.session['event_activated'] = eventlist.event.name
						request.session['event_id'] = eventlist.id
						return HttpResponseRedirect('/')
					except:
						return HttpResponseRedirect('/')
			else:
				context['check_errors'] = True
		else:
			context['check_errors'] = True

	return render_to_response('auth/login_form.html', context, context_instance=RequestContext(request)) 

def logout_user(request):
    logout(request)

    return HttpResponseRedirect(reverse('home'))

def admin_required(var):
    def wrap(request, *args, **kwargs):
    	if request.user.username != 'admin':
	        if request.user.newuser.usertype == 'n':
	            return HttpResponseRedirect('/')
            
        return var(request, *args, **kwargs)
    wrap.__doc__=var.__doc__
    wrap.__name__=var.__name__
    return wrap
