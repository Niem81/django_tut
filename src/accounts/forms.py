from django import forms
from django.contrib.auth import (
		authenticate,
		get_user_model,
		login,
		logout,
	)

User = get_user_model() # we will use this with the registration

class UserLoginForm(forms.Form):
	username = forms.CharField(label="Username/Email")
	password = forms.CharField(widget=forms.PasswordInput)

	# after a form is validated (with the is_valid() method) it runs a clean method
	def clean(self, *args, **kwargs): # you can add the args or kwargs if you dont know what the mthod recieves
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")

		# user_qs = User.objects.filter(username=username)
		# if user_qs.count() ==1:
		# 	user = user_qs.first()
		if username and password:
			user = authenticate(username=username, password=password)
			if not user.check_password(password):
				raise forms.ValidationError("Incorrect password")
			if not user:
				raise forms.ValidationError("This user does not exist.")
			if not user.is_active:
				raise forms.ValidationError("This user is no longer active.")
		return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
	# the var below is overriding the onw inside the model field
	email = forms.EmailField(label='Email Address')
	# adding a second email fiedl for email validation
	email2 = forms.EmailField(label='Confirm Email')
	password = forms.CharField(widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = [
			'username',
			'first_name',
			'last_name',
			'email',
			'email2',
			'password',
			'password2'
		]

	# def clean(self):
	# 	print(self.cleaned_data)
	# 	password = self.cleaned_data.get('password')
	# 	password2 = self.cleaned_data.get('password2')
	# 	if password != password2:
	# 		raise forms.ValidationError('Passwords must match!')

	# 	email = self.cleaned_data.get("email")
	# 	email2 = self.cleaned_data.get("email2")
	# 	print(email, email2)
	# 	if email != email2:
	# 		raise forms.ValidationError("Emails must match")
	# 	email_qs = User.objects.filter(email=email)
	# 	if email_qs.exists():
	# 		raise forms.ValidationError("This email is already registered.")
	# 	return super(UserRegisterForm, self).clean(*args, **kwargs)


	def clean_email2(self):
		print(self.cleaned_data)
		email = self.cleaned_data.get("email")
		email2 = self.cleaned_data.get("email2")
		print(email, email2)
		if email != email2:
			raise forms.ValidationError("Emails must match")
		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("This email is already registered.")
		return email

	def clean_password2(self):
		print(self.cleaned_data)
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		if password != password2:
			raise forms.ValidationError('Passwords must match!')

class ContactForm(forms.Form):
	name = forms.CharField(label = "Nombre")
	email = forms.EmailField(label = "Correo Electronico")
	
