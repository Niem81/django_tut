from django.contrib import admin

# Register your models here.

from .models import Post 
# we are getting the class
# se puede suprimir la palabra posts en posts.models por razon que se encuentra en el mismo folder

class PostModelAdmin(admin.ModelAdmin):
	list_display = ["title", "update", "timestamp"] 
	# we can leave it like unicode or change to title, so that will change the name from POST to TITLE
	list_display_links = ["update"]
	list_filter = ["update", "timestamp"]
	list_editable = ["title"]
	search_fields = ["title","content"]
	class Meta: 
		# class Meta refers to any non-field attribute - property of the class.
		model = Post




admin.site.register(Post, PostModelAdmin)