from braces.views import LoginRequiredMixin

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

from django.shortcuts import HttpResponseRedirect

from django.core.urlresolvers import reverse_lazy

from django.contrib.auth.models import User

from apps.blog.models import Tweet, HashTag
from apps.blog.forms import TweetForm


class ListTweets(ListView):
    """
    Get latest tweets
    """
    model = Tweet
    context_object_name = "tweets"
    paginate_by = 20


class ListTweetsByUser(DetailView):
    """
    Retrieve tweets for a particular User
    """
    model = User
    context_object_name = 'uzer'
    template_name = 'blog/tweet_list_user.html'


class CreateTweetView(LoginRequiredMixin, CreateView):
    """    
    Create a new Tweet by the current User (requires an authenticated user)
    """
    form_class = TweetForm
    model = Tweet
    success_url = reverse_lazy('blog:tweet-list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect(self.success_url)


class ListTweetsByHashTag(DetailView):
    """
    Retrieve tweets for a particular User
    """
    model = HashTag
    slug_url_kwarg = 'tag'
    slug_field = 'tag'
    context_object_name = 'hashtag'
    template_name = 'blog/tweet_list_hashtag.html'

