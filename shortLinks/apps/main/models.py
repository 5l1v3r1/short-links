import uuid

import short_url

from django.conf import settings
from django.db import models
from django.urls import reverse


class Link(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    origin_link = models.URLField(blank=False, null=False)
    datetime = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = 'link'
        verbose_name_plural = 'links'

    def get_absolute_url(self):
        return self.get_short_url

    @property
    def get_short_url(self):
        return reverse('main:redirect', kwargs={'short_link': short_url.encode_url(self.pk)})

    def __str__(self):
        return f'{self.origin_link}'


class Visit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    datetime = models.DateTimeField(auto_now_add=True, editable=False)
    link = models.ForeignKey(
        Link,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = 'visit'
        verbose_name_plural = 'visits'

    def __str__(self):
        return f'{self.datetime}'
