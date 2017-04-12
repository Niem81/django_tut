from django.conf.urls import url
from django.contrib import admin

# from . import views
from .views import (
	comment_detail,
	comment_delete
	)

urlpatterns = [
	# not using slug in here <slug>
    url(r'^(?P<id>\d+)/$', comment_detail, name='thread'), # comment_thread 
    url(r'^(?P<id>\d+)/delete/$', comment_delete, name='delete'), 
]