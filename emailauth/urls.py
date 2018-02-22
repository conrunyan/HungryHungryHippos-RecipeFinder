from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^', views.emailAuthPage, name='index'),
    #url(r'^sendemail/', views.sendEmail, name='email'),
]
