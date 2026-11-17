import logging
import re
from operator import itemgetter
from urllib.parse import quote

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from requests import HTTPError
from reversion import revisions
from social_core.backends.github import GithubOAuth2
from social_core.exceptions import InvalidEmail, SocialAuthBaseException
from social_core.pipeline.partial import partial
from social_django.middleware import SocialAuthExceptionMiddleware as OldSocialAuthExceptionMiddleware


from judge.forms import agreement_fields
from judge.models import Language, Profile
from judge.models.profile import GRADE_CHOICES, REGIONS

logger = logging.getLogger('judge.social_auth')


class GitHubSecureEmailOAuth2(GithubOAuth2):
    name = 'github-secure'

    def user_data(self, access_token, *args, **kwargs):
        data = self._user_data(access_token)
        try:
            emails = self._user_data(access_token, '/emails')
        except (HTTPError, ValueError, TypeError):
            emails = []

        emails = [(e.get('email'), e.get('primary'), 0) for e in emails if isinstance(e, dict) and e.get('verified')]
        emails.sort(key=itemgetter(1), reverse=True)
        emails = list(map(itemgetter(0), emails))

        if emails:
            data['email'] = emails[0]
        else:
            data['email'] = None

        return data


def slugify_username(username, renotword=re.compile(r'[^\w]')):
    return renotword.sub('', username.replace('-', '_'))


def verify_email(backend, details, *args, **kwargs):
    if not details['email']:
        raise InvalidEmail(backend)


class UsernameForm(forms.Form):
    """PNOI: the last step of signing up with Google."""
    username = forms.RegexField(regex=r'^\w+$', max_length=30, label='Username',
                                error_messages={'invalid': 'A username must contain letters, numbers, or underscores.'})
    school = forms.CharField(max_length=120, required=False, widget=forms.TextInput(attrs={
        'list': 'pn-school-names', 'autocomplete': 'off', 'placeholder': 'Start typing the name of your school'}))
    grade = forms.ChoiceField(required=False, choices=GRADE_CHOICES)
    region = forms.ChoiceField(required=False, choices=[('', 'Not set')] + list(REGIONS))
    age_ok, agree_rules = agreement_fields()

    def clean_username(self):
        if User.objects.filter(username__iexact=self.cleaned_data['username']).exists():
            raise forms.ValidationError('Sorry, the username is taken.')
        return self.cleaned_data['username']

    def clean_school(self):
        return Profile.clean_school_name(self.cleaned_data['school'])


@partial
def choose_username(backend, user, username=None, *args, **kwargs):
    if not user:
        request = backend.strategy.request
        if request.POST:
            form = UsernameForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                return {'username': data['username'], 'pnoi_school': data['school'],
                        'pnoi_grade': data['grade'], 'pnoi_region': data['region']}
        else:
            form = UsernameForm(initial={'username': username})
        return render(request, 'registration/username_select.html', {
            'title': 'Finish signing up', 'form': form, 'school_names': Profile.school_names(),
            'tos_url': settings.TERMS_OF_SERVICE_URL,
        })


def make_profile(backend, user, response, is_new=False, *args, **kwargs):
    # PNOI: everything was asked in the username step, so the profile is created without another form.
    if is_new and not hasattr(user, 'profile'):
        profile = Profile(user=user, language=Language.get_default_language(),
                          timezone=settings.DEFAULT_USER_TIME_ZONE)
        profile.school = kwargs.get('pnoi_school') or ''
        profile.region = kwargs.get('pnoi_region') or ''
        profile.set_grade_choice(kwargs.get('pnoi_grade') or '')
        with revisions.create_revision(atomic=True):
            profile.save()
            revisions.set_user(user)
            revisions.set_comment('Created on registration')


class SocialAuthExceptionMiddleware(OldSocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        if isinstance(exception, SocialAuthBaseException):
            return HttpResponseRedirect('%s?message=%s' % (reverse('social_auth_error'),
                                                           quote(self.get_message(request, exception))))
