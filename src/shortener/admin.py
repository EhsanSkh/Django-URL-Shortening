from django.contrib import admin
from shortener.models import URL


class URLAdmin(admin.ModelAdmin):
    readonly_fields = ["slug", "short_url"]


admin.site.register(URL, URLAdmin)
