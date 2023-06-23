from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User

from alert.models import Alert


def new_alert(request: HttpRequest):
    if request.method == "POST":
        emiter = request.user
        description = request.POST["content"]
        try:
            recipient = User.objects.filter(username__startswith=request.POST["recipient"])
        except:
            return HttpResponseBadRequest("Destinatário não existe: {}".format(request.POST["recipient"]))
        
        alert = Alert(emiter=emiter, description=description, recipients=recipient)
        return HttpResponse("Emiter: {}<br>Recipient: {}<br>Description: {}".format(emiter, recipient, description))

    return render(request, "alert/alert.html")
