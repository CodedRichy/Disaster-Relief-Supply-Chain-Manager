"""
URL configuration for disaster_relief project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from DRSCM import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('error404',views.error404),
    path('about',views.about),
    path('contact',views.contact),
    path('index',views.index),
    path('open',views.open),
    path('price',views.price),
    path('services',views.service),
    path('team',views.team),
    path('testimonial',views.testimonial),
]
