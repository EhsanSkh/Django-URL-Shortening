from django.conf import settings
from django.contrib import messages
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
    paginate_by = settings.PAGINATE_BY
    per_page_max = settings.PAGINATE_PER_PAGE_MAX

    def get_paginate_by(self, queryset):
        try:
            per_page = int(self.request.GET.get("perPage"))
            if per_page <= self.per_page_max:
                return per_page
            else:
                messages.warning(self.request, f"The maximum number for perPage is {self.per_page_max}.")
                return self.paginate_by
        except:
            return self.paginate_by

    def get_context_data(self, *args, **kwargs):
        context = super(URLShortenerListView, self).get_context_data(*args, **kwargs)
        try:
            per_page = int(self.request.GET.get("perPage"))
            if per_page <= self.per_page_max:
                context["per_page"] = str(per_page)
        except:
            context["per_page"] = None
        return context


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
