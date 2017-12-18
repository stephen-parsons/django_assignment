from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^friends$', views.index),
	url(r'^user/(?P<user_id>\d+)/friend$', views.add_friend),
	url(r'^user/(?P<user_id>\d+)/unfriend$', views.un_friend),
	url(r'user/(?P<user_id>\d+)$', views.user_profile)
]