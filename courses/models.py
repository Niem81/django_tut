from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Course(models.Model):
	created_at = models.DateTimeField(auto_now_add=True) #the auto_now_add will be set by the timezone from settings.py
	title = models.CharField(max_length=255)
	description = models.TextField()

	def __str__(self):
		return self.title

class Step(models.Model):
	title = models.CharField(max_length=255)
	description = models.TextField()
	content = models.TextField(blank=True, default='')
	order = models.IntegerField(default=0)
	course = models.ForeignKey(Course)

	class Meta:
		ordering = ['order',]

	def __str__(self):
		return self.title