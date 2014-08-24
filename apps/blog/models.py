import re

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.blog.templatetags.hashtag import pattern


class TweetManager(models.Manager):
    """
    Custom Manager for Tweet
    """

    def get_query_set(self, *args, **kwargs):
        """
        Override the default behaviour to prevent additional DB queries
        when accessing to the tweet's user
        """
        return super(TweetManager, self).get_query_set(*args, **kwargs).select_related()


class Tweet(models.Model):
    """
    Each Tweet contains :
    `user`: The owner
    `message`: The content of the tweet
    `created`: Date of creation, filled up automatically
    """
    user = models.ForeignKey(User, related_name='tweets')
    message = models.CharField(_('Tweet message'), max_length=140)
    created = models.DateTimeField(auto_now_add=True)

    # Override the Manager
    objects = TweetManager()

    class Meta:
        verbose_name = _('Tweet')
        verbose_name_plural = _('Tweets')
        ordering = ['-created']

    def __unicode__(self):
        return u'%s: %s' % (self.user.username, self.message)

    def save(self, *args, **kwargs):
        res = super(Tweet, self).save(*args, **kwargs)
        HashTag.build_tags(self)
        return res



class HashTag(models.Model):
    """
    Represents a HashTag (like Twitter or Facebook) wish is used in Tweet model
    `tag`: A unique HashTag over all database

    Example:
        This is a project powered by #django
    """
    tag = models.SlugField(_('HashTag'), max_length=30, unique=True, db_index=True)
    tweets = models.ManyToManyField(Tweet, related_name='tags')

    class Meta:
        verbose_name = _('HashTag')
        verbose_name_plural = _('HashTags')

    def __unicode__(self):
        return u'%s' % self.tag

    @classmethod
    def build_tags(cls, tweet):
        """
        Given a tweet, tries to pull out all available hashtags
        """
        for tag in re.findall(pattern, tweet.message):
            hashtag, _ = HashTag.objects.get_or_create(tag=tag)
            hashtag.tweets.add(tweet)
