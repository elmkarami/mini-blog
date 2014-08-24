from django.conf.urls import patterns, url

import views

from forms import LoginForm

urlpatterns = patterns('',
	url(r'user/(?P<pk>[\d]+)/?$', views.ListTweetsByUser.as_view(), name='user-tweet-list'),

	url(r'hashtag/(?P<tag>[-_\w]+)/?$', views.ListTweetsByHashTag.as_view(), name='hashtag-tweet-list'),

    url(r'^login/$', 'django.contrib.auth.views.login', {
            "template_name": "blog/login.html", 'authentication_form': LoginForm}, name='login-user'),	

    url(r'logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout-user'),

    url(r'new/?$', views.CreateTweetView.as_view(), name='tweet-create'),

    url(r'^$', views.ListTweets.as_view(), name='tweet-list'),

)
