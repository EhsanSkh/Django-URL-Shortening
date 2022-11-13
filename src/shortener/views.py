from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from shortener.forms import CreateShortURLForm
from shortener.mixins import StaffMixin
from shortener.models import URL


class URLShortenerListView(LoginRequiredMixin, generic.ListView):
    template_name = "shortener/list.html"
    model = URL
    context_object_name = "urls"


class URLShortenerCreateView(StaffMixin, generic.CreateView):
    template_name = "shortener/create.html"
    form_class = CreateShortURLForm
    success_url = reverse_lazy("shortener:list")

    def form_valid(self, form):
        url_obj = form.save(commit=False)
        url_obj.user = self.request.user
        return super(URLShortenerCreateView, self).form_valid(form)


class RedirectURLView(generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        url_obj = get_object_or_404(URL, slug=kwargs["slug"])
        return url_obj.main_url
