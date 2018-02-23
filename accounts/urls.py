from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/', views.login_view, name='login'),
    url(r'^register/', views.register_view, name='register'),
    url(r'^logout/', views.logout_view, name='logout'),
]
