from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect

from django.core.urlresolvers import reverse

from django.views.generic import ListView
from django.views.generic.base import View

from django.contrib.auth import login

from apps.blog.models import Tweet
from apps.blog.forms import LoginForm


class ListTweets(ListView):
    """
    Get latest tweets
    """
    model = Tweet
    context_object_name = "tweets"
    paginate_by = 20

    def get_queryset(self):
        return super(ListTweets, self).get_queryset()


class LoginView(View):
    """
    Class based view that handle user authentication
    """
    form_class = LoginForm
    template_name = 'blog/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(None, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect(reverse('blog:tweet-list'))
        return render(request, self.template_name, {'form': form})

