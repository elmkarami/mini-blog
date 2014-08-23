from django.conf.urls import patterns, url

import views


urlpatterns = patterns('',
	
	url(r'login/?$', views.LoginView.as_view(), name='login-user'),
    url(r'logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout-user'),
    url(r'^$', views.ListTweets.as_view(), name='tweet-list'),

)
