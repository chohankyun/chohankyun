# -*- coding: utf-8 -*-
from django.db import models


class Header(models.Model):
    title = models.CharField(max_length=100, blank=False)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'header'


class Footer(models.Model):
    copyright = models.CharField(max_length=100, blank=False)
    address = models.CharField(max_length=500, blank=False)
    phone = models.CharField(max_length=30, blank=False)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'footer'
