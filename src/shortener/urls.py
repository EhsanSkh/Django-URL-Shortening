from django.urls import path
from shortener import views

app_name = "shortener"

urlpatterns = [
    path("", views.URLShortenerListView.as_view(), name="list"),
    path("create/", views.URLShortenerCreateView.as_view(), name="create"),
    path("<slug:slug>/", views.RedirectURLView.as_view(), name="url"),
]
