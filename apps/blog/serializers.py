from rest_framework import serializers

from apps.blog.models import Tweet, HashTag


class TweetSerializer(serializers.ModelSerializer):
    user = serializers.RelatedField()
    tags = serializers.RelatedField(many=True)

    class Meta:
        model = Tweet
        fields = ('id', 'message','user', 'tags')


class HashTasgSerializer(serializers.ModelSerializer):

    label = serializers.SlugField(source='tag')
    value = serializers.IntegerField(source='id')

    class Meta:
        model = HashTag
        fields = ('label', 'value')
