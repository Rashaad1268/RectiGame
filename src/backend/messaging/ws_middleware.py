from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from channels.sessions import CookieMiddleware, SessionMiddleware


User = get_user_model()


def list_get(target_list, index):
    try:
        return target_list[0]
    except IndexError:
        return None


class URLParamAuthMiddleware(BaseMiddleware):
    """
    Token authorization middleware for Django Channels 2
    """

    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"].decode()
        query_dict = parse_qs(query_string)
        user = None

        if session_id := list_get(query_dict.get("authorization"), 0):
            try:
                session = await Session.objects.aget(pk=session_id)
                user_id = session.get_decoded()["_auth_user_id"]
                user = await User.objects.aget(id=user_id)
            except (Session.DoesNotExist, User.DoesNotExist):
                user = AnonymousUser()

        scope["user"] = user
        print("got user: ", user)

        return await super().__call__(scope, receive, send)


def WSMiddlewareStack(inner):
    return CookieMiddleware(SessionMiddleware(URLParamAuthMiddleware(inner)))
