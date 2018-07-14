# -*- coding: utf-8 -*-
from django.conf.urls import url

from home.views import CarouselList, PostListByOrder, MyPostListByOrder

urlpatterns = [
    url(r'^carousel/list/$', CarouselList.as_view(), name='home_carousel_list'),
    url(r'^post/list/(?P<order>\w+)/$', PostListByOrder.as_view(), name='home_post_list_by_order'),
    url(r'^my_post/list/(?P<order>\w+)/$', MyPostListByOrder.as_view(), name='home_my_post_list_by_order'),
]
