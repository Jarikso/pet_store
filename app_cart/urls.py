from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.cart_detail, name='cart_detail'),
    re_path(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
    re_path(r'^quick/(?P<product_id>\d+)/$', views.add_quick, name='quick'),
    re_path(r'^item_increment/(?P<product_id>\d+)/$', views.item_increment, name='item_increment'),
    re_path(r'^item_decrement/(?P<product_id>\d+)/$', views.item_decrement, name='item_decrement'),
    re_path(r'^remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
]