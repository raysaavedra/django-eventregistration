from django.conf.urls import patterns, include, url
from psitsregistration.views import *
from profiles.views import *
from auth.views import *
from registration.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r"^$", attend, name='home'),
    url(r'^create_account/$', create_account, name='create_account'),
    url(r'^add_student/$', add_student, name='add_student'),
    url(r'^event/$', event, name='event'),
    url(r'^event/create/$', create_event, name='create_event'),
    url(r'^event/activate/$', activate_event, name='activate_event'),
    url(r'^event/deactivate/$', deactivate_event, name='deactivate_event'),
    url(r'^attend/$', attend , name='attend'),
    url(r'^attend/search/$', ajax_search_lastname , name='ajax_search_lastname'),
    url(r'^attend/barcode/$', register_barcode , name='register_barcode'),
    url(r'^attend/register/$', register , name='register'),
    url(r'^attend/withdraw/$', withdraw , name='withdraw'),
    url(r'^attended/$', attended_form , name='attended_form'),
    url(r'^attended/search/school$', search_attended , name='search_attended'),
)

urlpatterns += patterns('',
    url(r'^login/$', login_user, name='login'),
    url(r'^logout/$', logout_user, name='logout'),
)
