from typing import Any

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from django.conf import settings
from django.contrib.auth.models import User

from backend.settings import EMAIL_PATTERN


def email_address(username: str) -> str:
    first_name = username.split()[0].lower()
    last_name = username.split()[-1].lower()

    email = EMAIL_PATTERN.format(first_name, last_name)
    count = User.objects.filter(email__startswith=email.split("@")[0]).count()

    if count != 0:
        return EMAIL_PATTERN.format(first_name, last_name + str(count))

    return email


def upload_img(file: Any, title: str, container="pictures"):
    ext = file.name.split(".")[-1]

    service_client = BlobServiceClient(
        settings.STORAGE_BUCKET, DefaultAzureCredential()
    )
    blob_client = service_client.get_blob_client(container, title)
    blob_client.upload_blob(file.read())
