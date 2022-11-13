from django import forms
from shortener.models import URL


class CreateShortURLForm(forms.ModelForm):
    class Meta:
        model = URL
        fields = ["main_url"]

    def clean_main_url(self):
        main_url = self.cleaned_data.get("main_url", None)
        if not main_url or URL.objects.filter(main_url=main_url).exists():
            short_url = URL.objects.get(main_url=main_url).short_url
            raise ValueError(f"This URL already has a short url:\n{short_url}")
        return main_url

    def __init__(self, *args, **kwargs):
        super(CreateShortURLForm, self).__init__(*args, **kwargs)
        self.fields["main_url"].widget.attrs["placeholder"] = "URL"
        self.fields["main_url"].widget.attrs["class"] = "form-control"
