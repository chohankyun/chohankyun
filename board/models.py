# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, blank=False)
    priority = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=200, blank=False)
    created_datetime = models.DateTimeField(auto_now_add=True)
    changed_datetime = models.DateTimeField(auto_now=True)


class Post(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subject = models.CharField(max_length=1000, blank=False)
    content = models.CharField(max_length=4000, blank=False)
    text_content = models.CharField(max_length=4000, blank=False)
    first_image_source = models.CharField(max_length=2000, blank=True)
    click_count = models.IntegerField()
    reply_count = models.IntegerField()
    recommend_count = models.IntegerField()
    created_datetime = models.DateTimeField(auto_now_add=True)
    changed_datetime = models.DateTimeField(auto_now=True)


class Reply(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=4000, blank=False)
    text_content = models.CharField(max_length=4000, blank=False)
    created_datetime = models.DateTimeField(auto_now_add=True)
    changed_datetime = models.DateTimeField(auto_now=True)


class Recommend(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now_add=True)
    changed_datetime = models.DateTimeField(auto_now=True)
