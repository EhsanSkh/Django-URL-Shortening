from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views as api_views

app_name = "api"

router = DefaultRouter()
router.register("", api_views.URLShortenerViewSet, basename="api-shortener")

urlpatterns = [
    path("register/", api_views.RegistrationAPIView.as_view(), name="register"),
    path("", include(router.urls)),
]
