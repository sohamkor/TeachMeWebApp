"""TeachMe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from teachingMainApp import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^signIn', views.authenticateUser, name='Page to authenticate the user'),
    url(r'^home', views.homePage, name='Home Page for the user'),
    url(r'^subjects', views.subjectsPage, name='Page that lists all the subjects'),
    url(r'^myClasses', views.myClassesPage, name='Page for all of the user\'s classes'),
    url(r'^rolloutAlgorithm', views.rolloutAlgorithmPage, name='Page to run the rollout algorithm'),
    url(r'^totalInfection', views.totalInfectionPage, name='Page to start a total infection'),
    url(r'^processTotalInfection', views.processTI, name='Page to process the total infection'),
    url(r'^tiSuccess', views.totalInfectionSucceeded, name='Page to let the user know that the total infection was successful'),
    url(r'^limitedInfection', views.limitedInfectionPage, name='Page to run the limited infection algorithm'),
    url(r'^processLimitedInfection', views.processLI, name='Page to process the limited infection'),
    url(r'^finishLimitedInfection', views.finishLI, name='Page to finish the limited infection'),
    url(r'^liSuccess', views.limitedInfectionSucceeded, name='Page to let the user know that the limited infection was successful'),
    url(r'^aboutUs', views.aboutUsPage, name='About us page'),
    url(r'^logout', views.logOut, name='Page to log out the user'),
]
