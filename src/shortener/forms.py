from django import forms
from shortener.models import URL


class CreateShortURLForm(forms.ModelForm):
    class Meta:
        model = URL
        fields = ["main_url"]

    def __init__(self, *args, **kwargs):
        super(CreateShortURLForm, self).__init__(*args, **kwargs)
        self.fields["main_url"].widget.attrs["placeholder"] = "URL"
        self.fields["main_url"].widget.attrs["class"] = "form-control"
