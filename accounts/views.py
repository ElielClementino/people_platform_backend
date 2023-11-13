from django.contrib import auth
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

from .service import accounts_svc


@csrf_protect
@require_POST
def login(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = auth.authenticate(username=username, password=password)
    user_dict = None
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            user_dict = _user_dict(user)
    return JsonResponse(user_dict, safe=False)


@csrf_protect
@require_POST
def register(request):
    account = accounts_svc.register(json.loads(request.body.decode()))
    return account


@require_POST
def logout(request):
    auth.logout(request)
    return JsonResponse({})


@ensure_csrf_cookie
def whoami(request):
    user_info = (
        {
            "user": _user_dict(request.user),
            "authenticated": True,
        }
        if request.user.is_authenticated
        else {"authenticated": False}
    )
    return JsonResponse(user_info)


def _user_dict(user):
    user_dict_info = {
        "id": user.id,
        "name": user.get_full_name(),
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "permissions": {
            "ADMIN": user.is_superuser,
            "STAFF": user.is_staff,
        },
    }

    return user_dict_info
