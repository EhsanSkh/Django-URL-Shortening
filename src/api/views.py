from rest_framework import generics, status
from rest_framework.response import Response
from api.serializers import UserRegistrationSerializer


class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "message": "User created successfully.",
            "status": status.HTTP_201_CREATED,
            "data": response.data
        })
