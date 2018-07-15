# -*- coding: utf-8 -*-
from django.conf.urls import url
from search.views import SearchPostByOrder

urlpatterns = [
    url(r'^post/(?P<search_word>.*)/(?P<order>\w+)/$', SearchPostByOrder.as_view(), name='search_post_by_order'),
]
