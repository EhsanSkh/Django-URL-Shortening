import string
import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save

User = get_user_model()


class URL(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="urls")
    main_url = models.URLField(max_length=500, unique=True,
                               error_messages={"unique": "Short URL for this URL already exists."})
    slug = models.SlugField()
    short_url = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created", "-id"]

    def __str__(self):
        return self.short_url


def create_short_url(size=8, chars=string.ascii_uppercase):
    domain = settings.DOMAIN
    slug = "".join([random.choice(chars) for _ in range(size)])
    if URL.objects.filter(slug=slug).exists():
        return create_short_url()
    else:
        short_url = domain + slug + "/"
        return slug, short_url


def post_save_create_short_url(sender, instance, created, *args, **kwargs):
    if created:
        instance.slug, instance.short_url = create_short_url()
        instance.save()


post_save.connect(post_save_create_short_url, sender=URL)
