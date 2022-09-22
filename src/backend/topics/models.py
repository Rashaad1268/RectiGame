from django.db import models
from django.utils.text import slugify
from django.conf import settings


class TopicTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding and not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50, blank=True, primary_key=True)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='topic/images')
    banner = models.ImageField(upload_to='topic/banners', null=True, blank=True)
    tags = models.ManyToManyField(TopicTag, blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding and not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)
