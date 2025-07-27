from django import forms

from mnrkr.models import MoonrakerConnection


class MoonrakerForm(forms.ModelForm):
    class Meta:
        model = MoonrakerConnection
        fields = ["url", "api_key"]
