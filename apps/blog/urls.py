from django.conf.urls import patterns, url
from django.conf import settings

from rest_framework import routers

import views
import api

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


router = routers.SimpleRouter()
router.register(r'api/tweets', api.TweetViewSet, base_name='api-tweet')
router.register(r'api/hashtags', api.HashTagViewSet, base_name='api-hashtag')
urlpatterns += router.urls



urlpatterns += patterns('', (r'^static/(.*)$',
							'django.views.static.serve',
							{ 'document_root': settings.STATIC_ROOT }),)