from django.forms import ModelForm
from .models import User


class StudentEnrollmentForm(ModelForm):
    template_name = "core/snippet.html"
    
    class Meta:
        model = User
        fields = "__all__"
