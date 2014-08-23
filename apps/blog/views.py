from braces.views import LoginRequiredMixin

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView

from django.shortcuts import HttpResponseRedirect

from django.contrib.auth.models import User

from apps.blog.models import Tweet
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
    form_class = TweetForm
    model = Tweet
    success_url = '/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect('/')
