import os
from datetime import datetime
from typing import Any

#from azure.identity import DefaultAzureCredential
#from azure.storage.blob import BlobServiceClient
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpRequest
from rolepermissions.checkers import has_role

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
    # ext = file.name.split(".")[-1]
    service_client = BlobServiceClient(
        #settings.STORAGE_BUCKET, DefaultAzureCredential()
    )
    blob_client = service_client.get_blob_client(container, title)
    blob_client.upload_blob(file.read())


def UTC_date(date: str):
    return datetime.strptime(date, "%Y-%m-%d").date()


def csv_data(line: bytes) -> list[str]:
    return line.decode().replace(os.linesep, "").replace("\n", "").split(",")


def read_csv(request: HttpRequest, file: str) -> tuple[list[list[str]], list[str]]:
    lines = list(map(csv_data, request.FILES[file].readlines()))
    return lines, lines.pop(0)


def dfilter(d: dict, keys: list[str]) -> dict:
    return {k: v for k, v in d.items() if k in keys}


def dexc(d: dict, keys: list[str]) -> dict:
    return {k: v for k, v in d.items() if k not in keys}


def get_coordinator(pk: str) -> User:
    coordinator = User.objects.get(username__startswith=pk)

    if not has_role(coordinator, ["coordinator", "admin", "teacher"]):
        raise Exception("Usuário {} não tem privilégios necessários".format(pk))

    return coordinator
