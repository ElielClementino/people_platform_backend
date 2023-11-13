from django.contrib.auth.models import User

def user_unknown():
    user_fixture = User.objects.create_user(
        id=1,
        username="unknown",
        first_name="user",
        last_name="unknown",
        email="unknown@example.com",
        password="unknown",
    )
    return user_fixture