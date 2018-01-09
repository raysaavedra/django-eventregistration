from django.contrib import admin
from profiles.models import *

class StudentAdmin(admin.ModelAdmin):
    list_display = ('studentID','firstname','lastname')

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'usertype')

admin.site.register(Student, StudentAdmin)
admin.site.register(NewUser, UserAdmin)