from django.db import models
from django.contrib.auth.models import User
#

GENDERS = (
        ('M', 'Male'),
        ('F', 'Female'),
)

YEARLEVELS = (
	  (1, '1'),
	  (2, '2'),
	  (3, '3'),
	  (4, '4'),
	  (5, '5'),
)

TYPE_OF_USER = (
        ('n', 'Normal'),
        ('a', 'Admin'),
)

class NewUser(User):
	usertype = models.CharField(max_length=100, choices=TYPE_OF_USER)

	def __unicode__(self):
		return self.username

class Student(models.Model):
	studentID = models.IntegerField(unique=True)
	lastname = models.CharField(max_length=30)
	firstname = models.CharField(max_length=30)
	gender = models.CharField(max_length = 10, choices=GENDERS)
	school = models.CharField(max_length=60)
	year = models.IntegerField(choices=YEARLEVELS)

	def __unicode__(self):
		return str(self.studentID)

class Event(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField(null=True,blank=True)
	date_start = models.DateField()

	def __unicode__(self):
		return self.name


class EventList(models.Model):
	account = models.ForeignKey(NewUser)
	event = models.ForeignKey(Event)
	activated = models.BooleanField(default=False)

	def __unicode__(self):
		return str(self.event.name)




