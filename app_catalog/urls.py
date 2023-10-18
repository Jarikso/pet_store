from django.urls import path
from .views import MainListView, AllListView, ProductDetail

urlpatterns = [
    path('', MainListView.as_view(), name='main_page'),
    path('catalog/', AllListView.as_view(), name="product_list"),
    path('catalog/<slug:slug>/', ProductDetail.as_view(), name='goods')
]
