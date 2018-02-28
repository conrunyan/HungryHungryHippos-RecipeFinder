from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^activate/', views.emailAuthPage, name='activate'),
    #url(r'^error/', views.sendEmail, name='email')
]
