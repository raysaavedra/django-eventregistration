from django.template import Context
from django.template.loader import get_template
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from profiles import models
from registration import forms
from registration.models import attendance
from django.db import connection
import datetime
from django.contrib.auth.decorators import login_required
import re
from django.utils.timezone import utc

@login_required(login_url='/login')
def attend(request):
    context = {}
    context['studform'] = forms.StudentForm()

    return render_to_response('registration/attendance.html',context,context_instance=RequestContext(request))

@login_required(login_url='/login')
def ajax_search_lastname(request):
    context = {}
    cursor = connection.cursor() 

    if request.is_ajax():
        search = request.GET.get('q')
        if search is not None:
            try:
                eventlist_id = request.session.get('event_id')
                cursor.execute("SELECT profiles_student.studentID, profiles_student.lastname, profiles_student.firstname, profiles_student.gender, profiles_student.school, profiles_student.year, registration_attendance.id as attendid from psitsregistration.profiles_student left join psitsregistration.registration_attendance on (psitsregistration.registration_attendance.event_id = %s and psitsregistration.registration_attendance.student_id = profiles_student.id)where (psitsregistration.profiles_student.lastname like %s)",(eventlist_id,(search + "%")))
                results = cursor.fetchall()
            except Exception as e:
                print e
            context['students'] = results

            if len(results) == 0:
                context['message'] = "Your search yielded no results"

    return render_to_response('registration/student.html',context,context_instance=RequestContext(request))

@login_required(login_url='/login')
def register_barcode(request):
    context = {}
    context['studform'] = forms.StudentForm()

    if request.is_ajax():
        idnum = request.GET.get('q')
        if idnum is not None:
            temp1 = re.sub(r'[^\w]', '', idnum)     # removes special character
            idfinal = temp1[9:]
            #temp2 = re.compile("220..00(\d\d\d\d\d\d)")
            #temp2 = re.compile("201..TS(\d\d\d\d\d)")
            #idfinal = temp2.match(temp1)  # match the barcode from the regex function
            
            if idfinal is not None:
                studID = idfinal
                eventlist_id = request.session.get('event_id')
                if eventlist_id is not None:
                    event = models.EventList.objects.get(pk=eventlist_id)
                    student = models.Student.objects.get(studentID = studID)
                    stud_attend = attendance.objects.filter(student=student,event=event)
                    if len(stud_attend) == 0:
                        attend = attendance.objects.create(student=student,event=event,time_in=datetime.datetime.utcnow().replace(tzinfo=utc))
                        attend.save()
                        context['message'] = "Student ID {0} : Successfully Registered".format(str(studID))
                    else:
                        context['message'] = "Student ID {0} is already registered.".format(str(studID))
            else:
                context['message'] = "Error reading barcode!"
    return render_to_response('registration/student.html',context,context_instance=RequestContext(request))

@login_required(login_url='/login')
def register(request):
    context_instance=RequestContext(request)

    if request.is_ajax():
        idnum = request.GET.get('q')
        if idnum is not None:
            try:
                eventlist_id = request.session.get('event_id')
                if eventlist_id is not None:
                    event = models.EventList.objects.get(pk=eventlist_id)
                    student = models.Student.objects.get(studentID = idnum)
                    stud_attend = attendance.objects.filter(student=student,event=event)
                    if len(stud_attend) == 0:
                        attend = attendance.objects.create(student=student,event=event,time_in=datetime.datetime.utcnow().replace(tzinfo=utc))
                        attend.save()
                        data = simplejson.dumps(True)
                        return HttpResponse(data, mimetype='application/javascript')
            except Exception as e:            
                data = simplejson.dumps(e)
                return HttpResponse(data, mimetype='application/javascript')

@login_required(login_url='/login')
def withdraw(request):
    context_instance=RequestContext(request)

    if request.is_ajax():
        q = request.GET.get('q')
        if q is not None:
            try:
                eventlist_id = request.session.get('event_id')
                if eventlist_id is not None:
                    e = models.EventList.objects.get(pk=eventlist_id)
                    attend = attendance.objects.get(student__studentID__exact=q, event=e)
                    attend.delete()     # delete from database
                    data = simplejson.dumps(True)
                    return HttpResponse(data, mimetype='application/javascript')
            except Exception as e:
                data = simplejson.dumps(e)
                return HttpResponse(data, mimetype='application/javascript')

@login_required(login_url='/login')
def attended_form(request):
    context={}
    context['school'] = models.Student.objects.values('school').distinct().order_by('school')

    return render_to_response('registration/attended.html',context,context_instance=RequestContext(request))

@login_required(login_url='/login')
def search_attended(request):
    context = {}
    if request.is_ajax():
        q = request.GET.get('q')
        if q is not None:
            eventlist_id = request.session.get('event_id')
            if q == '%':
                results = attendance.objects.filter(event=eventlist_id).order_by('time_in')
            else:
                print 'w'
                results = attendance.objects.filter(student__school=q,event=eventlist_id).order_by('time_in')

            context['students'] = results
            
            if len(results) == 0:
                context['message'] = "Your search yielded no results"
            return render_to_response('registration/student_attended.html',context,context_instance=RequestContext(request))

@login_required(login_url='/login')
def search_school_attended(request):
    context = {}
    if request.is_ajax():
        q = request.GET.get('q')
        print q
        if q is not None:
            eventlist_id = request.session.get('event_id')
            if q == '%':
                results = attendance.objects.filter(event=eventlist_id).order_by('time_in')
            else:
                results = attendance.objects.filter(student__school=q,event=eventlist_id).order_by('time_in')

            context['students'] = results
            
            if len(results) == 0:
                context['message'] = "Your search yielded no results"
            return render_to_response('registration/student_attended.html',context,context_instance=RequestContext(request))