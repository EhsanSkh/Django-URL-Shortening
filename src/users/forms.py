from django import forms
from django.contrib.auth import get_user_model


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}))

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "confirm_password"]

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match!"
            )

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = f"Email Address"
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = f"Email Address"
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
