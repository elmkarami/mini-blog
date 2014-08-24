from django.contrib.auth.forms import AuthenticationForm

from django import forms

from apps.blog.models import Tweet


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(TweetForm, self).__init__(*args, **kwargs)
        self.fields['message'].widget= forms.Textarea(attrs={'rows': 3, 'cols': 10})
        self.fields['message'].widget.attrs['class'] = "form-control"

    def clean_message(self):
        """
        Prevent getting only withspaces in `message` field
        """
        return self.cleaned_data.get('message', '').strip()


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = "form-control"
        self.fields['password'].widget.attrs['class'] = "form-control"
