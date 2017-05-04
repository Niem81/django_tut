from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Contact(models.Model):
    TOPICS = (
		('CONSULT', 'Consulting'),
		('BLOG', 'Blog'),
		('CONTRACT', 'Services'),
        ('FOOD', 'Food Preparation'),
		('OTHER', 'Others')
	)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    message = models.TextField()
    topic = models.CharField(choices=TOPICS, max_length=200)
    publish = models.DateField(auto_now=False, auto_now_add=False)
