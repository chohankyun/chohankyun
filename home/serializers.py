# -*- coding: utf-8 -*-
from rest_framework import serializers

from home.models import Carousel


class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = '__all__'
