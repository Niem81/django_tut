from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Contact(models.Model):
    TOPICS = (
		('CONSULT', 'Consulting'),
		('BLOG', 'Blog'),
		('CONTRACT', 'Services'),
		('OTHER', 'Others')
	)
    name = models.CharField()
    email = models.EmailField()
    message = models.TextField()
    topic = models.CharField(choices=TOPICS)
	publish = models.DateField(auto_now=False, auto_now_add=False)
