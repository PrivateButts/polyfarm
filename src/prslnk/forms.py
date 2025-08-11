from django import forms

from prslnk.models import PrusaLinkConnection


class PrusaLinkForm(forms.ModelForm):
    class Meta:
        model = PrusaLinkConnection
        fields = ["url", "api_key"]
