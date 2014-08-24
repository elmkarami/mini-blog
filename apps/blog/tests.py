"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import json
from model_mommy import mommy

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User

from django.core.urlresolvers import reverse

from django.test.client import Client
from django.test import TestCase

from apps.blog.models import Tweet, HashTag
from apps.blog.forms import TweetForm
from apps.blog.views import ListTweets
from apps.blog.templatetags.hashtag import hashtagify
from apps.blog.serializers import HashTasgSerializer



class ListTweetsViewTest(TestCase):

    def setUp(self):
        self.first_tweet = mommy.make(Tweet)
        self.tweets = mommy.make(Tweet, _quantity=ListTweets.paginate_by)

    def test_listing_tweets_with_no_tweet(self):
        Tweet.objects.all().delete()
        client = Client()
        response = client.get(reverse('blog:tweet-list'))
        self.assertIn('No Tweet available', response.content)

    def test_listing_tweets(self):
        client = Client()
        response = client.get(reverse('blog:tweet-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Tweet.objects.all().count(), ListTweets.paginate_by + 1)

    def test_order_by_created(self):
        client = Client()
        response = client.get(reverse('blog:tweet-list'))
        self.assertNotIn(self.first_tweet.message, response.content)

    def test_pagination_tweets(self):
        client = Client()
        response = client.get('%s?page=%s' % (reverse('blog:tweet-list'), 2))
        self.assertIn(self.first_tweet.message, response.content)


class ListTweetsByUserViewTest(TestCase):
    def setUp(self):
        self.first_user = mommy.make(User)
        self.second_user = mommy.make(User)
        mommy.make(Tweet, user=self.first_user, _quantity=1)
        mommy.make(Tweet, user=self.second_user, _quantity=1)

    def test_list_tweets_by_user(self):
        client = Client()
        response = client.get(reverse('blog:user-tweet-list', args=[self.first_user.pk]))
        self.assertIn(self.first_user.tweets.all()[0].message, response.content)
        self.assertNotIn(self.second_user.tweets.all()[0].message, response.content)


class CreateTweetViewTest(TestCase):

    def test_add_tweet_by_anonymous_user(self):
        client = Client()
        client.post(reverse('blog:tweet-create'), {'message':'test tweet'})
        self.assertEqual(Tweet.objects.all().count(), 0)

    def new_user(self):
        user = mommy.prepare(User, username='karami')
        user.set_password('mehdi')
        user.save()
        self.user = user

    def test_tweet_form(self):
        form = TweetForm(data={'message':'   ', 'user':mommy.make(User)})
        self.assertFalse(form.is_valid())

    def test_add_withespace_tweet_by_authenticated_user(self):
        self.new_user()
        client = Client()
        client.login(username='karami', password='mehdi')
        client.post(reverse('blog:tweet-create'), {'message':'  '})
        self.assertEqual(Tweet.objects.filter(user=self.user).count(), 0)        

    def test_add_tweet_by_authenticated_user(self):
        self.new_user()
        client = Client()
        client.login(username='karami', password='mehdi')
        client.post(reverse('blog:tweet-create'), {'message':'test tweet'})
        self.assertEqual(Tweet.objects.filter(user=self.user).count(), 1)


class HashTagTest(TestCase):

    def test_add_tweet_without_hashtags(self):
        Tweet.objects.create(message="Simple tweet", user=mommy.make(User))
        self.assertFalse(HashTag.objects.all().exists())

    def test_add_tweet_with_hashtags(self):
        Tweet.objects.create(message="This is a #tweet #test", user=mommy.make(User))
        self.assertEqual(HashTag.objects.all().count(), 2)
        self.assertEqual(HashTag.objects.filter(tag='tweet').count(), 1)
        self.assertEqual(HashTag.objects.filter(tag='test').count(), 1)

    def test_hashtagify(self):
        tweet = 'Simple #tweet for #django'
        url_django = reverse('blog:hashtag-tweet-list', args=['django'])
        url_tweet= reverse('blog:hashtag-tweet-list', args=['tweet'])
        expected ='Simple <a href="%s">#tweet</a> for <a href="%s">#django</a>' % (url_tweet, url_django)
        self.assertEqual(hashtagify(tweet), expected)

    def test_list_tweet_by_hashtag(self):
        tweet = 'Tweet #test'
        tweet2 = 'another #tweet'
        Tweet.objects.create(message=tweet, user=mommy.make(User))
        Tweet.objects.create(message=tweet2, user=mommy.make(User))
        client = Client()
        response = client.get(reverse('blog:hashtag-tweet-list', args=['test']))
        self.assertIn(hashtagify(tweet), response.content)
        self.assertNotIn(hashtagify(tweet2), response.content)        


class TweetAPIViewTest(TestCase):
    def setUp(self):
        mommy.make(Tweet, _quantity=3)

    def test_list_tweets_by_anonymous_users(self):
        client = APIClient()
        response = client.get(reverse('blog:api-tweet-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_tweets_by_authenticated_users(self):
        user = mommy.make(User)
        client = APIClient() 
        client.credentials(HTTP_AUTHORIZATION='Token ' + Token.objects.get(user=user).key)
        response = client.get(reverse('blog:api-tweet-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class HashTagAPIViewTest(TestCase):
    def create_tags(self):
        HashTag.objects.create(tag='python')
        HashTag.objects.create(tag='django')
        HashTag.objects.create(tag='tweet')
        HashTag.objects.create(tag='project')

    def test_filter_tags(self):
        self.create_tags()
        client = APIClient() 
        response = client.get('%s?term=p' % reverse('blog:api-hashtag-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = HashTasgSerializer(HashTag.objects.filter(tag__icontains='p'), many=True)
        self.assertEqual(json.loads(response.content), serializer.data)
