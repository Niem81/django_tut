from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Contact(models.Model):
    TOPICS = (
		('TC', 'Tecnologia'),
		('PR', 'Programacion'),
		('IN', 'Innovacion'),
		('OT', 'Others')
	)
    name = models.CharField()
    email = models.EmailField()
    message = models.TextField()
    topic = models.CharField(choices=TOPICS)
