# -*- coding: utf-8 -*-
from django.contrib import admin
from board.models import Category, Post, Reply


class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ['created_datetime', 'changed_datetime']
    list_display = [field.name for field in Category._meta.fields]


admin.site.register(Category, CategoryAdmin)


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ['created_datetime', 'changed_datetime']
    list_display = [field.name for field in Post._meta.fields if field.name != 'content']


admin.site.register(Post, PostAdmin)


class ReplyAdmin(admin.ModelAdmin):
    readonly_fields = ['created_datetime', 'changed_datetime']
    list_display = [field.name for field in Reply._meta.fields if field.name != 'content']


admin.site.register(Reply, ReplyAdmin)
