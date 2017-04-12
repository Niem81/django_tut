from django import forms

from .models import Comment

# to use ModelForm, we must specify a model inside this class

class CommentForm(forms.Form):
	content_type = forms.CharField(widget=forms.HiddenInput)
	object_id = forms.IntegerField(widget=forms.HiddenInput)
	# parent_id = forms.IntegerField(widget=forms.HiddenInput, require=False) # this is going to be related to replies 
	content = forms.CharField(label='', widget=forms.Textarea)