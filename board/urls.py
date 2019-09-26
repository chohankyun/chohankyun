# -*- coding: utf-8 -*-
from django.conf.urls import url

from board.views import CategoryList, PostDetail, PostCreate, PostUpdate, PostDelete
from board.views import PostListByCategoryNOrder, MyPostListByCategoryNOrder, PostIncreaseClickCount
from board.views import RecommendCountNOwner, RecommendCreate, RecommendDelete
from board.views import ReplyCreate, ReplyList, ReplyDelete, ReplyUpdate

urlpatterns = [
    url(r'^category/list/$', CategoryList.as_view(), name='board_category_list'),
    url(r'^post/list/(?P<category>\w+)/(?P<order>\w+)/$', PostListByCategoryNOrder.as_view(), name='board_post_list_by_category_n_order'),
    url(r'^my_post/list/(?P<category>\w+)/(?P<order>\w+)/$', MyPostListByCategoryNOrder.as_view(), name='board_my_post_list_by_category_n_order'),
    url(r'^post/detail/(?P<pk>\w+)/$', PostDetail.as_view(), name='board_post_detail'),
    url(r'^post/create/$', PostCreate.as_view(), name='board_post_create'),
    url(r'^post/update/(?P<pk>\w+)/$', PostUpdate.as_view(), name='board_post_update'),
    url(r'^post/delete/(?P<pk>\w+)/$', PostDelete.as_view(), name='board_post_delete'),
    url(r'^post/increase_click_count/(?P<pk>\w+)/$', PostIncreaseClickCount.as_view(), name='board_post_increase_click_count'),
    url(r'^reply/create/$', ReplyCreate.as_view(), name='board_reply_create'),
    url(r'^reply/list/(?P<post_id>\w+)/$', ReplyList.as_view(), name='board_reply_list'),
    url(r'^reply/update/(?P<pk>\w+)/$', ReplyUpdate.as_view(), name='board_reply_update'),
    url(r'^reply/delete/(?P<pk>\w+)/$', ReplyDelete.as_view(), name='board_reply_delete'),
    url(r'^recommend/count/(?P<post_id>\w+)/$', RecommendCountNOwner.as_view(), name='board_recommend_count_n_owner'),
    url(r'^recommend/create/$', RecommendCreate.as_view(), name='board_recommend_create'),
    url(r'^recommend/delete/(?P<post_id>\w+)/$', RecommendDelete.as_view(), name='board_recommend_delete'),
]
