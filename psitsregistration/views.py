from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template import Context
from django.template.loader import get_template
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def home(request):
    context = {}

    return render_to_response('index.html', context, RequestContext(request))