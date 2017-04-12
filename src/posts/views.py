try: # python 2
	from urllib import quote_plus
except:
	pass

try: # python 3
	from urllib.parse import quote_plus
except:
	pass

from django.contrib.auth.decorators import login_required
from django.contrib import messages
# adding ContentType to use comments inside post_detail
# this is after adding the contenttype in comments.models
from django.contrib.contenttypes.models import ContentType
# the line above is being commented as we start using managers, but reuse again with Commentform
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import datetime

# importing the Comment class
from comments.models import Comment

# importiny the CommentForm
from comments.forms import CommentForm
# Create your views here.
from .forms import PostForm
from .models import Post
# importing the utility of reading words per minute
# from .utils import get_read_time
@login_required
def posts_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	if not request.user.is_authenticated():
		raise Http404

	form = PostForm(request.POST or None, request.FILES or None)
	print form
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		print "HOHOHOHOHOHOHOHOHOHOHOHOHOHOHOH"
		print instance
		print "HOHOHOHOHOHOHOHOHOHOHOHOHOHOHOH"
		print form.cleaned_data.get("title")
		instance.save()
		# message success
		messages.success(request, "Successfully Created!")
		return HttpResponseRedirect(instance.get_absolute_url())
	# if request.method == 'POST':
	# 	print request.POST.get("content")
	# 	print request.POST.get("title")
		# Post.objects.create(title=title)
	context = {
		"form":form,
	}
	# return HttpResponse("<h1>Create</h1>") #render()
	return render(request, "post_form.html", context)

# @login_required
def posts_detail(request, slug=None):
	
	# if not request.user.is_staff or not request.user.is_superuser:
		# raise Http404
	# validando si existe un usuario autenticado
	valido = True
	if not request.user.is_authenticated():
		print "Change to False"
		valido = False

	# instance = Post.objects.get(id=1)
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	
	print "Instance Detail"
	print instance.user
	share_string = quote_plus(instance.content)

	# printing the words per minute
	# print(get_read_time(instance.content))
	# print(get_read_time(instance.get_markdown()))

	# the 2 lines below are commented because we are using managers and no longer contenttype
	# content_type = ContentType.objects.get_for_model(Post) #the model itself is the Post model
	# obj_id = instance.id # its the post_id
	# what the previous is doing is Post.objects.get(id=instance.id)
	# the line below: replace filter with filter_by_instance when start using managers
	# also replace content_type=content_type, object_id=obj_id with just instance. This part is now handle in models
	comments = instance.comments #Comment.objects.filter_by_instance(instance)

	# adding the comment form and initial data
	initial_data = {
		'content_type': instance.get_content_type,
		'object_id': instance.id
	}
	form = CommentForm(request.POST or None, initial= initial_data)
	if form.is_valid() and request.user.is_authenticated():
		# print(comment_form.cleaned_data)
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get("object_id")
		content_data = form.cleaned_data.get("content")
		# adding the parent_id for the comments
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None
		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count()==1:
				parent_obj = parent_qs.first()

		new_comment, created = Comment.objects.get_or_create(
				user= request.user, 
				content_type= content_type,
				object_id= obj_id, 
				content= content_data,
				parent= parent_obj
			)
		print(new_comment, created)
		if created:
			print("Yeah it worked!")
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	context = {
		'data':instance.title,
		'instance':instance, 
		'share_string': share_string,
		'valido':valido,
		'comments': comments,
		'comment_form': form
	}
	# return HttpResponse("<h1>Detail</h1>") #render()
	return render(request, "post_detail.html", context)

def posts_list(request):
	today = timezone.now().date()
	# queryset_list = Post.objects.filter(draft=False).filter(publish__lte=timezone.now()) #.all().order_by("-timestamp")
	# queryset_list = Post.objects.all() #.order_by("-timestamp") #all already override in PostManager
	queryset_list = Post.objects.active() #now its active due to be able to see the drafts
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()

	query = request.GET.get('q')
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(user__first_name__icontains=query)|
			Q(user__last_name__icontains=query)			
			).distinct() #distinct is for not having duplicate items
	paginator = Paginator(queryset_list, 3) # Show 25 contacts per page
	page_request_var = "papiro"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	print(request.user)


	context = {
		'object_list':queryset,
		'data':'Viva el Codigo! Wey tu eres un bot o anonimo!',
		'page_request_var':page_request_var,
		'today':today
	}

	# response = render(request, "post_list.html", context)
	# visits = int(request.COOKIES.get('visits', '0'))

	# # Does the cookie last_visit exist?
	# if 'last_visit' in request.COOKIES:
 #        # Yes it does! Get the cookie's value.
	# 	last_visit = request.COOKIES['last_visit']
 #        # Cast the value to a Python date/time object.
	# 	last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

 #        # If it's been more than a day since the last visit...
	# 	if (datetime.now() - last_visit_time).days > 0:
 #            # ...reassign the value of the cookie to +1 of what it was before...
	# 		response.set_cookie('visits', visits+1)
	# 		print (response.COOKIES.get('visits'))
 #            # ...and update the last visit cookie, too.
	# 		response.set_cookie('last_visit', datetime.now())
	# else:
 #        # Cookie last_visit doesn't exist, so create it to the current date/time.
	# 	response.set_cookie('last_visit', datetime.now())

	#### NEW CODE ####
	if request.session.get('last_visit'):
        # The session has a value for the last visit
		last_visit_time = request.session.get('last_visit')
		visits = request.session.get('visits', 0)

		if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
			request.session['visits'] = visits + 1
			request.session['last_visit'] = str(datetime.now())
	else:
        # The get returns None, and the session does not have a value for the last visit.
		request.session['last_visit'] = str(datetime.now())
		request.session['visits'] = 1
    #### END NEW CODE ####
	print (request.session['visits'], request.session['last_visit'])


	# ahora definamos una condicional si el usuario esta o no logueado
	# if request.user.is_authenticated():
	# 	context = {'data':'Viva el Codigo!'}
	# else:
	# 	context = {'data':'Viva el Codigo! Wey tu eres un bot o anonimo!'}
	# return HttpResponse("<h1>List</h1>") #render()
	# return render(request, "base.html", context)
	return render(request, "post_list.html", context)

@login_required
def posts_update(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance = instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		# message success
		messages.success(request, "<a href='#'>Item</a> Updated!", extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		'data':instance.title,
		'instance':instance,
		'form':form,
	}
	# return HttpResponse("<h1>Update</h1>") #render()
	return render(request, "post_form.html", context)

@login_required
def posts_delete(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	messages.success(request, "Item Deleted!")
	return redirect('posts:list')
	# return HttpResponse("<h1>Delete</h1>") #render()






