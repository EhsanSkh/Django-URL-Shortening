from django.conf import settings
from rest_framework import filters, generics, status, viewsets
from rest_framework import exceptions
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

    def get_paginated_response(self, data):
        return Response({
            "message": "Successful" if self.page.paginator.count > 0 else "There is no URLs.",
            "count": self.page.paginator.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "data": data
        })

    def paginate_queryset(self, queryset, request, view=None):
        paginator = self.django_paginator_class(queryset, self.get_page_size(request))
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages
        try:
            paginator.page(page_number)
        except Exception as exc:
            msg = {
                "message": "There is no URLs.",
                "data": []
            }
            raise exceptions.NotFound(msg)
        return super(URLsPagination, self).paginate_queryset(queryset, request, view=None)


class URLShortenerViewSet(viewsets.ModelViewSet):
    serializer_class = URLShortenerSerializer
    queryset = URL.objects.all().select_related("user")
    pagination_class = URLsPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["main_url", "user__email"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "message": "Short URL created.",
            "data": response.data,
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        url_obj = self.get_queryset().filter(slug=kwargs.get("pk")).first()
        if not url_obj:
            return Response({
                "message": "There is no short URL for this URL.",
                "data": "",
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(url_obj)
        return Response({
            "message": "Successful",
            "data": serializer.data,
        })

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsAuthenticated]
        elif self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        return super(URLShortenerViewSet, self).get_permissions()
