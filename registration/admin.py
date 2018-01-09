from django.contrib import admin
from registration.models import *

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student','event','time_in')


admin.site.register(attendance, AttendanceAdmin)