from django.contrib.auth import login
from django.contrib.auth.models import User
from django_slack_oauth.models import SlackUser


def register_slack_user(request, data):
    if data.get('ok'):
        user, _ = User.objects.get_or_create(
            username=data['user']['id'],
            defaults={
                'email': data['user']['email'],
                'last_name': data['user']['name'],
            },
        )
        if user.is_active:
            slacker, _ = SlackUser.objects.get_or_create(slacker=user)
            slacker.access_token = data.pop('access_token')
            slacker.extras = data
            slacker.save()
            login(request, user)
    return request, data
