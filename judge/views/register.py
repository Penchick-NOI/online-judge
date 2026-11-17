# coding=utf-8
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import get_default_password_validators
from django.core.cache import cache
from django.forms import ChoiceField
from django.shortcuts import render
from django.utils.translation import gettext, gettext_lazy as _
from registration.backends.default.views import (ActivationView as OldActivationView,
                                                 RegistrationView as OldRegistrationView,
                                                 ResendActivationView as OldResendActivationView)
from registration.forms import RegistrationForm

from judge.forms import agreement_fields
from judge.models import Language, Profile, TIMEZONE
from judge.models.profile import GRADE_CHOICES, REGIONS
from judge.utils.mail import validate_email_domain
from judge.utils.recaptcha import ReCaptchaField, ReCaptchaWidget
from judge.utils.subscription import Subscription, newsletter_id
from judge.widgets import Select2Widget


class CustomRegistrationForm(RegistrationForm):
    username = forms.RegexField(regex=r'^\w+$', max_length=30, label=_('Username'),
                                error_messages={'invalid': _('A username must contain letters, '
                                                             'numbers, or underscores.')})
    timezone = ChoiceField(label=_('Timezone'), choices=TIMEZONE,
                           widget=Select2Widget(attrs={'style': 'width:100%'}))
    school = forms.CharField(label=_('School'), max_length=120, required=False,
                             widget=forms.TextInput(attrs={
                                 'list': 'pn-school-names', 'autocomplete': 'off',
                                 'placeholder': _('Start typing the name of your school'),
                             }))
    grade = ChoiceField(label=_('Grade level'), required=False, choices=GRADE_CHOICES)
    region = ChoiceField(label=_('Region'), required=False, choices=[('', _('Not set'))] + list(REGIONS))
    age_ok, agree_rules = agreement_fields()

    if newsletter_id is not None:
        newsletter = forms.BooleanField(label=_('Subscribe to newsletter?'), initial=True, required=False)

    if ReCaptchaField is not None:
        captcha = ReCaptchaField(widget=ReCaptchaWidget())

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(gettext('The email address "%s" is already taken. Only one registration '
                                                'is allowed per address.') % self.cleaned_data['email'])
        validate_email_domain(self.cleaned_data['email'])
        return self.cleaned_data['email']

    def clean_school(self):
        return Profile.clean_school_name(self.cleaned_data['school'])


class RegistrationView(OldRegistrationView):
    title = _('Register')
    form_class = CustomRegistrationForm
    template_name = 'registration/registration_form.html'

    def get_context_data(self, **kwargs):
        if 'title' not in kwargs:
            kwargs['title'] = self.title
        kwargs['TIMEZONE_MAP'] = settings.TIMEZONE_MAP
        kwargs['password_validators'] = get_default_password_validators()
        kwargs['tos_url'] = settings.TERMS_OF_SERVICE_URL
        kwargs['school_names'] = Profile.school_names()
        kwargs['has_google_auth'] = bool(getattr(settings, 'SOCIAL_AUTH_GOOGLE_OAUTH2_KEY', None) and
                                         getattr(settings, 'SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET', None))
        return super(RegistrationView, self).get_context_data(**kwargs)

    def register(self, form):
        user = super(RegistrationView, self).register(form)
        profile, _ = Profile.objects.get_or_create(user=user, defaults={
            'language': Language.get_default_language(),
        })

        cleaned_data = form.cleaned_data
        profile.timezone = cleaned_data['timezone']
        profile.school = cleaned_data['school']
        profile.region = cleaned_data['region']
        profile.set_grade_choice(cleaned_data['grade'])
        profile.save()

        if newsletter_id is not None and cleaned_data['newsletter']:
            Subscription(user=user, newsletter_id=newsletter_id, subscribed=True).save()
        return user

    def get_initial(self, *args, **kwargs):
        initial = super(RegistrationView, self).get_initial(*args, **kwargs)
        initial['timezone'] = settings.DEFAULT_USER_TIME_ZONE
        return initial


class ActivationView(OldActivationView):
    title = _('Activation Key Invalid')
    template_name = 'registration/activate.html'

    def get_context_data(self, **kwargs):
        if 'title' not in kwargs:
            kwargs['title'] = self.title
        return super(ActivationView, self).get_context_data(**kwargs)


class ResendActivationView(OldResendActivationView):
    """PNOI: send a new confirmation link to an account that has not been confirmed yet."""
    template_name = 'registration/resend_activation_form.html'

    def get_context_data(self, **kwargs):
        kwargs.setdefault('title', _('Confirm your email'))
        return super(ResendActivationView, self).get_context_data(**kwargs)

    def resend_activation(self, form):
        # At most three new links an hour for one address, so the form cannot be used to flood an inbox.
        key = 'pnoi_resend_activation:%s' % form.cleaned_data['email'].lower()
        count = cache.get(key, 0)
        if count >= 3:
            return False
        cache.set(key, count + 1, 3600)
        return super(ResendActivationView, self).resend_activation(form)

    def render_form_submitted_template(self, form):
        # The same answer whether or not the address exists, so the form does not reveal who has an account.
        return render(self.request, self.template_name, {'title': _('Confirm your email'), 'sent': True})


def social_auth_error(request):
    return render(request, 'generic-message.html', {
        'title': gettext('Authentication failure'),
        'message': request.GET.get('message'),
    })
