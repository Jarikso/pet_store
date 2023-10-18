from django.urls import path
from .views import make_order, pay_order, progress_pay, HistoryOrders, OnlyOrder

urlpatterns = [
    path('', make_order, name='make_order'),
    path('payment/<int:pk>', pay_order, name='payment'),
    path('progress-pay/<int:pk>', progress_pay, name='progress_pay'),
    path('history/<int:pk>', HistoryOrders.as_view(), name='history'),
    path('only-order/<int:pk>', OnlyOrder.as_view(), name='only_order'),
]