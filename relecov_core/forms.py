from django import forms
from .models import MarkDownModel


class MarkedDownExampleForm(forms.ModelForm):
    class Meta:

        model = MarkDownModel
        fields = "__all__"
