from django.contrib import admin

from apps.blog.models import Tweet, HashTag


class TweetAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created')
    ordering = ('-created',)


admin.site.register(HashTag)
admin.site.register(Tweet, TweetAdmin)

