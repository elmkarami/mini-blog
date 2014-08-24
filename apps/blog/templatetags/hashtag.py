import re

from bleach import clean

from django import template

from django.core.urlresolvers import reverse


register = template.Library()

pattern = re.compile(r'#([-_\w]+)')


def hashtagify(value):
    """
    Converts hashtags into clickable links.

    Example:
        "This #project is powered by #django" will be :
        "This <a href='/hashtag/project'>#project</a> <a href='/hashtag/django'>#django</a>

    But no worries this will not allow for example XSS attacks since we use
    the bleach library to keep just the `a` tags, so all others tags will be escaped
    """
    return clean(re.sub(pattern,
    					r'<a href="%s\1">#\1</a>' % reverse('blog:hashtag-tweet-list', args=['-'])[:-1],
    					value), ['a'])


register.filter(hashtagify)