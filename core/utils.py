from django.contrib.auth.models import User
from backend.settings import EMAIL_PATTERN


def email_address(username: str) -> str:
    first_name = username.split()[0].lower()
    last_name = username.split()[-1].lower()

    email = EMAIL_PATTERN.format(first_name, last_name)
    count = User.objects.filter(email__starts_with=email.split("@")[0])

    if count != 0:
        return EMAIL_PATTERN.format(first_name, last_name + str(count))

    return email
