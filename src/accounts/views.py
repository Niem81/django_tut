from django.contrib.auth import (
		authenticate,
		get_user_model,
		login,
		logout,
	)

from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import datetime

from .forms import UserLoginForm, UserRegisterForm, ContactForm
from .models import Contact
# Create your views here.

def login_view(request):
	print(request.user.is_authenticated())
	next = request.GET.get('next')
	title = "Login"
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		login(request, user)
		if next:
			return redirect(next)
		print(request.user.is_authenticated())
		return redirect('/')

	return render(request, "form.html", {"form":form, "title":title})

def register_view(request):
	print(request.user.is_authenticated())
	next = request.GET.get('next')
	title = "Register"
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		print (user)
		if user.is_anonymous():
			print 'User is is_anonymous'
		new_user = authenticate(username=user.username, password=password)
		print(new_user)
		print 'hola'
		login(request, new_user)
		if next:
			return redirect(next)
		#return
		return redirect('/')
	else:
		print form.errors

	context = {
		"form": form,
		"title": title
	}
	return render(request, "form.html", context)

def logout_view(request):
	logout(request)
	# return render(request, "form.html", {})
	return redirect('/')

def full_contact(request):
	print("Enter contact info")
	next = request.GET.get('next')
	title = "Contact"
	form = ContactForm(request.POST or None)
	if form.is_valid():
		print("passing validation")
		contacto = form.save(commit=False)
		contacto.save()
		if next:
			return redirect(next)
		#return
		return redirect('/contact')
	else:
		print form.errors
	context = {
		"form": form,
		"title": title
	}
	return render(request, "contact.html", context)

def home_view(request):
	print("Go into home view")
	today = timezone.now().date()
	return render(request, "home.html")
