# -*- coding: utf-8 -*-
from django.contrib import admin
from home.models import Carousel


class CarouselAdmin(admin.ModelAdmin):
    readonly_fields = ['created_datetime', 'changed_datetime']
    list_display = [field.name for field in Carousel._meta.fields]


admin.site.register(Carousel, CarouselAdmin)
