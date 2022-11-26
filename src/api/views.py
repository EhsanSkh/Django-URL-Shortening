from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, status, viewsets
from rest_framework.pagination import PageNumberPagination
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
            "data": response.data
        }, status=status.HTTP_201_CREATED)


class URLsPagination(PageNumberPagination):
    page_size = settings.API_PAGINATE_BY
    max_page_size = settings.API_PAGINATE_PER_PAGE_MAX
    page_size_query_param = "perPage"


class URLShortenerViewSet(viewsets.ModelViewSet):
    serializer_class = URLShortenerSerializer
    queryset = URL.objects.all()
    pagination_class = URLsPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["main_url", "user__email"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        url_obj = get_object_or_404(URL, slug=kwargs.get("pk"))
        serializer = URLShortenerSerializer(url_obj)
        return Response({
            "data": serializer.data
        })

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsAuthenticated]
        elif self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super(URLShortenerViewSet, self).get_permissions()
