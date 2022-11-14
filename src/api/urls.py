from django.urls import path
from api import views as api_views

app_name = "api"

urlpatterns = [
    path("register/", api_views.RegistrationAPIView.as_view(), name="register"),
]
