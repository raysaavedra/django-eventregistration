from django.db import models
from profiles.models import *
# Create your models here.

class attendance(models.Model):
	time_in = models.DateTimeField()
	student = models.ForeignKey(Student)
	event = models.ForeignKey(EventList)