from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.

# we no longer use the Post model as we are handlind what its comming by instance
# from posts.models import Post

class CommentManager(models.Manager):
	def all(self):
		qs = super(CommentManager, self).filter(parent=None)
		return qs

	def filter_by_instance(self, instance):
		# as we are dealing with the instance, we are changing the Post with the class of the refer instance that its being passed
		content_type = ContentType.objects.get_for_model(instance.__class__)# (Post) #the model itself is the Post model
		obj_id = instance.id # its the post_id
		# what the previous is doing is Post.objects.get(id=instance.id)
		# comments = Comment.objects.filter(content_type=content_type, object_id=obj_id)
		# the previuos is no longer going to be used , using querysets
		qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id).filter(parent=None)
		# the above is like getting an instance of Comments.objects || adding a second filter for the parent
		return qs

class Comment(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	# post = models.ForeignKey(Post)

	# this 3 below will take place of the post item
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	
	# adding a parent element for the replies
	parent = models.ForeignKey("self", null=True, blank=True)

	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

	# the objects from Comment are being replace for what its in CommentManager
	objects = CommentManager()

	class Meta:
		ordering = ['-timestamp']

	def __unicode__(self):
		return str(self.user.username)

	def __str__(self):
		return str(self.user.username)

	def get_absolute_url(self):
		return reverse("comments:thread", kwargs={"id":self.id})

	def get_delete_url(self):
		return reverse("comments:delete", kwargs={"id":self.id})

	# creating the children comment associated to the parent comment
	def children(self):
		return Comment.objects.filter(parent=self)

	# determine if the comment is the parent
	@property
	def is_parent(self):
		if self.parent is not None:
			return False
		return True

