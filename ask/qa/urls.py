from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import logout

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.login_u, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^question/(?P<num_question>\d+)/$', views.question, name='question'),
    url(r'^ask/', views.ask, name='ask'),
    url(r'^popular/', views.popular, name='popular'),
    url(r'^new/', views.new, name='new'),
]
