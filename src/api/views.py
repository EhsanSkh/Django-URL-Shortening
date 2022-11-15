from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from api.serializers import UserRegistrationSerializer, URLShortenerSerializer
from shortener.models import URL


class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "message": "User created successfully.",
            "status": status.HTTP_201_CREATED,
            "data": response.data
        })


class URLShortenerViewSet(viewsets.ModelViewSet):
    serializer_class = URLShortenerSerializer
    queryset = URL.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        url_obj = get_object_or_404(URL, slug=kwargs.get("pk"))
        serializer = URLShortenerSerializer(url_obj)
        return Response({
            "status": status.HTTP_200_OK,
            "data": serializer.data
        })

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsAuthenticated]
        elif self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super(URLShortenerViewSet, self).get_permissions()
