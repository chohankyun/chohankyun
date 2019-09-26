# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from django.forms import TextInput

from home.models import Carousel


class CarouselAdmin(admin.ModelAdmin):
    readonly_fields = ['created_datetime', 'updated_datetime']
    list_display = [field.name for field in Carousel._meta.fields]

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '150'})},
    }


admin.site.register(Carousel, CarouselAdmin)
