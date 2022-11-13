from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View, generic
from users import forms


class RegisterView(generic.FormView):
    template_name = "users/register.html"
    form_class = forms.UserRegistrationForm
    success_url = reverse_lazy("shortener:list")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(email=email, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, "Account created successfully. You are logged in.")
        else:
            return super(RegisterView, self).form_invalid(form)

        return super(RegisterView, self).form_valid(form)


class LoginView(generic.FormView):
    template_name = "users/login.html"
    form_class = forms.UserLoginForm
    success_url = reverse_lazy("shortener:list")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(email=email, password=password)
        if user is None:
            messages.error(self.request, "Invalid Credentials.")
            return super(LoginView, self).form_invalid(form)
        else:
            login(self.request, user)
            messages.success(self.request, "You are logged in.")

        return super(LoginView, self).form_valid(form)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(self.request, "You are logged out.")
        return redirect("users:login")

