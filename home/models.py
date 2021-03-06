# -*- coding: utf-8 -*-
from django.db import models


class Carousel(models.Model):
    image_source = models.CharField(max_length=500, blank=False, help_text="이미지 크기 8 : 2 비율 사용.")
    priority = models.CharField(max_length=1, blank=False, default=0, help_text="사용(1, 2, 3), 사용안함(0)")
    description = models.CharField(max_length=200, blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carousel'

        indexes = [
            models.Index(fields=['priority']),
        ]
