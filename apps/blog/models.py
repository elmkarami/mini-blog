from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class TweetManager(models.Manager):

    def get_query_set(self, *args, **kwargs):
        return super(TweetManager, self).get_query_set(*args, **kwargs).select_related()


class Tweet(models.Model):
    user = models.ForeignKey(User, related_name='tweets')
    message = models.CharField(_('Tweet message'), max_length=140)
    created = models.DateTimeField(auto_now_add=True)

    objects = TweetManager()

    class Meta:
        verbose_name = _('Tweet')
        verbose_name_plural = _('Tweets')
        ordering = ['-created']

    def __unicode__(self):
        return u'%s: %s' % (self.user.username, self.message)
