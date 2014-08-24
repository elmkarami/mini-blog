"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from model_mommy import mommy

from django.contrib.auth.models import User

from django.core.urlresolvers import reverse

from django.test.client import Client
from django.test import TestCase

from apps.blog.models import Tweet


class ListTweetsViewTest(TestCase):
    def setUp(self):
        self.first_tweet = mommy.make(Tweet)
        self.tweets = mommy.make(Tweet, _quantity=20)

    def test_listing_tweets_with_no_tweet(self):
        Tweet.objects.all().delete()
        client = Client()
        response = client.get(reverse('blog:tweet-list'))
        self.assertIn('No Tweet available', response.content)

    def test_listing_tweets(self):
        client = Client()
        response = client.get(reverse('blog:tweet-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Tweet.objects.all().count(), 21)

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

    def test_add_tweet_by_authenticated_user(self):
        self.new_user()
        client = Client()
        client.login(username='karami', password='mehdi')
        client.post(reverse('blog:tweet-create'), {'message':'test tweet'})
        self.assertEqual(Tweet.objects.filter(user=self.user).count(), 1)

