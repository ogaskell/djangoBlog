#!/usr/bin/env python3

from django.urls import path
from . import views

urlpatterns = [
    path('',views.post_list, name='post_list'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('like/', views.store_like, name="like"),
    path('comment/', views.store_comment, name="comment"),
    path('post/', views.single_post, name='post')
]
