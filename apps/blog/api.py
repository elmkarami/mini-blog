from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from apps.blog.models import Tweet, HashTag
from apps.blog.serializers import TweetSerializer, HashTasgSerializer
from apps.blog.filters import HashTagFilter


class TweetViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for listing lastest tweets
    """
    model = Tweet
    serializer_class = TweetSerializer
    paginate_by = 20
    permission_classes = (permissions.IsAuthenticated, )    


class HashTagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for listing all hashtags (used for autocompletion)
    """
    model = HashTag
    serializer_class = HashTasgSerializer

    def list(self, request):
        qs = HashTagFilter(request.GET, HashTag.objects.all())
        serializer = HashTasgSerializer(qs, many=True)
        return Response(serializer.data)
