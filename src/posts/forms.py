from django import forms

from pagedown.widgets import PagedownWidget

from .models import Post

# for adding labels , help_texts
from django.utils.translation import ugettext_lazy as _

class PostForm(forms.ModelForm):
	content = forms.CharField(widget=PagedownWidget(show_preview=False))
	publish = forms.DateField(widget=forms.SelectDateWidget)
	class Meta:
		model = Post
		fields = [
			'title',
			'content',
			'post_topic',
			'post_classif',
			'image',
			'draft',
			'publish'
		]
		labels = {
			'title': _('Type the Title of this Post:'),
			'post_topic': _('Select the Topic of your Post:'),
			'post_classif':_('Select the Type of Post - Adult or Public')
		}
		help_texts = {
            'title': _('Add some words main subject.'),
            'content': _('Display all the content related to the subject.'),
        }
        widgets = {
        	'title': forms.TextInput(attrs = {'placeholder': 'Add some words as main subject.'})
        }