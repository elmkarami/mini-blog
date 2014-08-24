from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


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
