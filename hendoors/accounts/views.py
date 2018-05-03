from urllib.parse import urlencode
import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LogoutView as BaseLogOutView
from django.core.cache import cache
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.generic import RedirectView, TemplateView
import requests


UserModel = get_user_model()


class LogInView(TemplateView):
    template_name = 'accounts/log_in.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        next_url = self.request.GET.get('next')
        context['next_url'] = '?next={}'.format(next_url) if next_url else ''
        return context


@method_decorator(never_cache, name='dispatch')
class SlackLogInView(RedirectView):
    CACHE_PREFIX = 'accounts:slack-oauth-state:'

    def get_cache_key(self, state):
        return '{}{}'.format(self.CACHE_PREFIX, state)

    def get_oauth_redirect_uri(self):
        return self.request.build_absolute_uri(reverse('accounts:slack-log-in'))

    def get_oauth_authorize_url(self, state):
        data = {
            'client_id': settings.SLACK_CLIENT_ID,
            'scope': settings.SLACK_SCOPE,
            'redirect_uri': self.get_oauth_redirect_uri(),
            'state': state,
            'team': 'T0Z0A0L21',
        }
        return 'https://slack.com/oauth/authorize?{}'.format(urlencode(data))

    def get_oauth_access(self, code):
        return requests.get('https://slack.com/api/oauth.access', {
            'client_id': settings.SLACK_CLIENT_ID,
            'client_secret': settings.SLACK_CLIENT_SECRET,
            'code': code,
            'redirect_uri': self.get_oauth_redirect_uri(),
        })

    def get_redirect_url(self, *args, **kwargs):
        code = self.request.GET.get('code')
        state = self.request.GET.get('state')
        if None in (code, state):
            state = ''.join(str(uuid.uuid4()).split('-'))
            state_data = {'next': self.request.GET.get('next', '')}
            cache.set(self.get_cache_key(state), state_data)
            return self.get_oauth_authorize_url(state)

        cache_key = self.get_cache_key(state)
        state_data = cache.get(cache_key)
        if state_data is None:
            messages.error(self.request, 'Invalid state')
            return reverse('accounts:log-in')

        cache.delete(cache_key)

        response = self.get_oauth_access(code)
        if response.status_code != 200:
            messages.error(self.request, 'OAuth access failed')
            return reverse('accounts:log-in')

        data = response.json()
        if not data.get('ok'):
            messages.error(self.request, 'OAuth access failed')
            return reverse('accounts:log-in')

        if not self.authenticate(data):
            messages.error(self.request, 'Could not complete authentication')
            return reverse('accounts:log-in')

        url_is_safe = is_safe_url(
            url=state_data['next'],
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure(),
        )
        if url_is_safe:
            return state_data['next']
        return reverse(settings.LOGIN_REDIRECT_URL)

    def authenticate(self, data):
        user, _ = UserModel.objects.get_or_create(
            email=data['user']['email'],
        )
        if not user.is_active:
            return False
        name = data['user']['name']
        if name:
            user.name = name
        user.extras = data
        user.save()
        login(self.request, user)
        return True


class LogOutView(BaseLogOutView):
    template_name = 'accounts/log_out.html'
