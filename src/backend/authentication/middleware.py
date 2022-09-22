from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
# from rest_framework.response import Response


class BannedUsersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not hasattr(request, 'user'):
            raise Exception(('request.user attribute is not set\n'
                             'Make sure BannedUsersMiddleware is placed after AuthenticationMiddleware'))

        user = request.user
        if user.is_authenticated:
            if user.disabled_until is not None:
                if user.disabled_until > timezone.now():
                    return JsonResponse({'detail': f'Account is disabled until {user.disabled_until.strftime("%Y-%m-%d %H:%M:%S")}',
                                         'until': user.disabled_until}, status=status.HTTP_403_FORBIDDEN)

        return self.get_response(request)
