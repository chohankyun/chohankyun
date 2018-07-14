"""chohankyun URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='static/index.html', permanent=True)),
    url(r'^admin/', admin.site.urls),
    url(r'^rest-auth/', include('auth_extend.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^home/', include('home.urls')),
    url(r'^index/', include('index.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^board/', include('board.urls')),
]
