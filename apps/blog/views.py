from django.views.generic import ListView

from apps.blog.models import Tweet


class ListTweets(ListView):
    """
    Get latest tweets
    """
    model = Tweet
    context_object_name = "tweets"
    paginate_by = 20

    def get_queryset(self):
        return super(ListTweets, self).get_queryset()
