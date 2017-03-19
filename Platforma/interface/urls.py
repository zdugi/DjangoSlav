from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^about$', views.about, name='about'),
	url(r'^login$', views.login, name='login'),
	url(r'^logout$', views.logout, name='logout'),
	url(r'^register$', views.register, name='register'),
	url(r'^support$', views.support, name='support'),
	url(r'^platform$', views.platform, name='platform'),
	url(r'^platform/(\d+)/$', views.platform_page, name='platform_page'),
	url(r'^ServicePlatform$', views.service, name='service'),
]
