"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# for integration with static files like css js img
from django.conf import settings
from django.conf.urls.static import static

# from original
from django.conf.urls import url, include
from django.contrib import admin

# for redirecting to other url
from django.views.generic import RedirectView

# importing the
from accounts.views import (login_view, register_view, logout_view, home_view, full_contact)

urlpatterns = [

    url(r'^ultra/adminyoyolala/', admin.site.urls),
    # borrar el dolar xqe sino afectara al patron de include,
    # url(r'^posts/$', <appname>.views.<function_name>),
	# url(r'^', RedirectView.as_view(url='/posts/')),
    # adding the comments url
    url(r'^comments/', include("comments.urls", namespace='comments')),
    url(r'^goin/login/', login_view, name='login'),
    url(r'^goin/logout/', logout_view, name='logout'),
    url(r'^goin/register/', register_view, name='register'),
    url(r'^blog/', include("posts.urls", namespace='posts')),
    url(r'^', home_view, name='home'),
    url(r'^contact/', full_contact, name='contact')
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
