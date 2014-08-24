import django_filters

from models import HashTag


class HashTagFilter(django_filters.FilterSet):

    term = django_filters.CharFilter(name="tag", lookup_type='icontains')

    class Meta:
        model = HashTag
        fields = ['term']
