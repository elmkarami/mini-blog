from django.conf.urls import patterns, url

import views


urlpatterns = patterns('',

    url(r'^$', views.ListTweets.as_view(), name='tweet-list'),

)
