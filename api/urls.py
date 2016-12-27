"""api URL Configuration

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
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf.urls import url, include
# from api.views import home


urlpatterns = [
    # The normal jazz here...
    # url(r'^blog/', include('api.urls')),
    # url(r'^$', home, name='home'),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
]
