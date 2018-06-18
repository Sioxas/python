"""Image URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from home import views as home_views

urlpatterns = [
    url(r'^$', home_views.index),
    url(r'^register/', home_views.register),
    url(r'^login/', home_views.login),
    url(r'^post/', home_views.post),
    url(r'^share/', home_views.share),
    url(r'^myShareList/', home_views.myShareList),
    url(r'^hotShareList/', home_views.hotShareList),
    url(r'^allShareList/', home_views.allShareList),
    url(r'^admin/', admin.site.urls),
]
