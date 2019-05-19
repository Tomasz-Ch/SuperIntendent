"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from superintendent.views import StartView, NewMenuView, MenuView, SchoolUpdate

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', StartView.as_view(), name="index"),
    path('new_menu/', NewMenuView.as_view(), name="new-menu"),
    path('obiady/', MenuView.as_view(), name="obiady"),
    path('szkola/<pk>', SchoolUpdate.as_view(), name="school"),
]
