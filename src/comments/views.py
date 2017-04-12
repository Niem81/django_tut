from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404

from .forms import CommentForm
from .models import Comment

# Create your views here.

# we are adding a decorator for the user ve able to login if wants to add coment
@login_required(login_url='/login/') # i can comment the login_url part by adding a LOGIN_URL in settings
def comment_delete(request, id):
	# obj = get_object_or_404(Comment, id=id)
	try:
		obj = Comment.objects.get(id=id)
	except:
		raise Http404

	if obj.user != request.user:
		# messages.success(request, "You don't have permission to perform this task.")
		# raise Http404
		response = HttpResponse("You don't have permission to perform this task.")
		response.status_code = 403
		return response
		# return render(request, "comment_delete.html", context, status_code=403)

	if request.method == "POST":
		parent_obj_url = obj.content_object.get_absolute_url()
		obj.delete()
		messages.success(request, "This comment Has been Deleted!")
		return HttpResponseRedirect(parent_obj_url)
	context = {
		'object': obj
	}
	return render(request, "comment_delete.html", context)

def comment_detail(request, id):
	# obj = get_object_or_404(Comment, id=id)
	try:
		obj = Comment.objects.get(id=id)
	except:
		raise Http404

	if not obj.is_parent:
		obj = obj.parent


	content_object = obj.content_object # Post that the comment is on
	content_id = obj.content_object.id
	initial_data = {
		'content_type': obj.content_type,# content_object.get_content_type,
		'object_id': obj.object_id # content_id
	}
	form = CommentForm(request.POST or None, initial= initial_data)
	# print(dir(form))
	# print(form.errors)
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
		'cmnt': obj,
		'form': form
	}
	return render(request, "comment_detail.html", context)




