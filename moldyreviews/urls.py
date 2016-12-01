from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	url(r'^$', views.home_site, name='home'),
	url(r'^ratings/$', views.rating_list, name='rating_list'),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^rating/new/$', views.rating_new, name="rating_new"),
	url(r'^rating/(?P<pk>\d+)/$', views.rating_detail, name='rating_detail'),
	url(r'^rating/(?P<pk>\d+)/edit/$', views.rating_edit, name='rating_edit'),
	url(r'^login/', auth_views.login, {'template_name':'movierating/login.html'}, name='login'),
	url(r'^rating/(?P<pk>\d+)/remove/$', views.rating_remove, name='rating_remove'),
	url(r'^accounts/profile/$', views.login_success, name='login_redirect'),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^signup/success/$', views.register_success, name="register_success"),
	url(r'^reports/$',views.report_view,name="report_view"),
	url(r'^reports/(?P<pk>\d+)/$', views.report_detail, name='report_detail'),
]