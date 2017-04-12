from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
# we bring ContentType for the @property get_content_type
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.utils.text import slugify
from django.utils.safestring import mark_safe

from comments.models import Comment
from markdown_deux import markdown

from .utils import get_read_time
# Create your models here.
#MVC

# type of manager
# Post.objects.all()
# Post.objects.create(user=user, title='title')
class PostManager(models.Manager):
	# def all(self, *args, **kwargs):
	def active(self, *args, **kwargs):
		# Post.objects.all() = super(PostManager, self).all()
		return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())

def upload_location(instance, filename):
	# filebase, extension = filename.split('.')
	# return "%s/%s.%s" %(instance.id, instance.id, extension)
	return "%s/%s" %(instance.slug, filename)

class Post(models.Model):
	TOPICS = (
		('TC', 'Tecnologia'),
		('PR', 'Programacion'),
		('IN', 'Innovacion'),
		('OT', 'Others')
	)
	CLASSIFICATION = (
		('AD', 'Adulto',),
		('PU', 'Apto Para Todos')
	)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	title = models.CharField(max_length=120)
	slug = models.SlugField(unique=True)
	# image = models.FileField(null=True, blank=True)
	image = models.ImageField(upload_to=upload_location,
		null=True, blank=True, 
		width_field="width_field", 
		height_field="height_field")
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	content = models.TextField()
	post_topic = models.CharField(max_length=2, choices=TOPICS)
	post_classif = models.CharField(max_length=2, choices=CLASSIFICATION)
	draft = models.BooleanField(default=False)
	publish = models.DateField(auto_now=False, auto_now_add=False)
	read_time = models.IntegerField(default=0) # models.TimeField(null=True, blank=True)
	update = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	objects = PostManager()

	def __unicode__(self):
		return self.title

	# en python 3:
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		# return reverse("posts:detail", kwargs={"id":self.id})
		return reverse("posts:detail", kwargs={"slug":self.slug})
		# return "/posts/%s/" %(self.id)

	def get_markdown(self):
		content = self.content
		return mark_safe(markdown(content))

	class Meta:
		ordering = ["-timestamp", "-update"]

	@property
	def comments(self):
		instance = self
		qs = Comment.objects.filter_by_instance(instance)
		return qs

	@property
	def get_content_type(self):
		# we are using again content type as we want to get the content type of this model below
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type

def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug=slug).order_by("-id")
	print qs
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
	# slug = slugify(instance.title)
	# # change the title to "Tesla item 1" -> "tesla-item-1"
	# exists = Post.objects.filter(slug=slug).exists()
	# if exists:
	# 	slug = "%s-%s" %(slug, instance.id)
	# instance.slug = slug
	if not instance.slug:
		instance.slug = create_slug(instance)
	if instance.content:
		html_string = instance.get_markdown()
		read_time_var = get_read_time(html_string)
		instance.read_time = read_time_var

pre_save.connect(pre_save_post_receiver, sender=Post)


