from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.generic import ListView
from lists.models import List
from django.conf import settings
from django.contrib import admin

from alllists.views import hello
from . import views

urlpatterns = [
	url(r'^lists/$', views.homepage_console, name='homepage_console'),
	#url(r'^changed/$', TemplateView.as_view(template_name="4m.html")),
	#url(r'^added/$', views.added),
	
	url(r'^$', views.homepage_console, name='homepage_console'),
	url(r'^create/$', views.list_create, name='list_create'),
  	#url(r'^new$', views.list_create, name='list_new'),
  	url(r'^delete/(?P<pk>\d+)$', views.list_delete, name='list_delete'),
  	url(r'^create/(?P<pk>\d+)$', views.list_create_child, name='list_create_child'),
  	url(r'^undo/$', views.undo_last_action, name='undo_last_action'),
  	url(r'^nuke/$', views.nuke_it_all, name='nuke_it_all'),
  	url(r'^tab/(?P<pk>\d+)$', views.list_tab, name='list_tab'),
  	url(r'^untab/(?P<pk>\d+)$', views.list_untab, name='list_untab'),
]