from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from app_account.forms import CreationUserForm
from app_catalog.models import Product
from app_cart.cart import Cart

from .models import OrderItem, Order


def make_order(request):
    cart = Cart(request)
    if request.user.is_authenticated:
        if request.method == 'POST':
            value = request.POST
            record = Order.objects.create(user_id=request.user.id, full_name=value['full_name'], phone=value['phone'],
                                          email=value['mail'], city=value['city'], address=value['address'],
                                          delivery='OR' if value['delivery'] == "Обычная доставка" else 'EX',
                                          pay_method='MC' if value['pay'] == "Онлайн картой" else 'AC',
                                          price=cart.get_total_price())
            for data in cart:
                OrderItem.objects.create(order=record, product=Product.objects.get(id=data['id']),
                                         quantity=data['quantity'])
            cart.clear()
            return redirect('order:payment', pk=record.id)
        else:
            return render(request, 'app_orders/order_create.html', {'cart': cart})

    elif not request.user.is_authenticated:
        if request.method == 'POST':
            user_form = CreationUserForm(request.POST)
            if user_form.is_valid():
                user_form.save()  # zaq12wsx33 - password
                email = user_form.cleaned_data.get('email')
                password = user_form.cleaned_data.get('password1')
                user = authenticate(email=email, password=password)
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('/order')
        else:
            user_form = CreationUserForm()
        return render(request, 'app_orders/order_create.html', {'signup': user_form})
    else:
        return render(request, 'app_orders/order_create.html')


def pay_order(request, pk):
    order = Order.objects.get(pk=pk)
    if request.method == 'POST':
        card_num = ''.join(request.POST['numero1'].split(' '))
        if (len(card_num) == 8) and (card_num[-1:] != '0') and (int(card_num) % 2 == 0):
            Order.objects.filter(pk=pk).update(paid=True)
        return redirect('order:progress_pay', pk=order.id)
    return render(request, 'app_orders/order_pay.html', {'method': order.pay_method})


def progress_pay(request, pk):
    status = Order.objects.get(pk=pk).paid
    if status:
        messages.success(request, 'Оплата прошла успешно')
    else:
        messages.success(request, 'Оплата не прошла т.к. карта не соответсвует требованиям оплаты. Вернитесь в '
                                  'главное меню и повторите оплату заказа через личный кабинет')
    return render(request, 'app_orders/order_progress_pay.html')


class HistoryOrders(LoginRequiredMixin, View):

    def get(self, request, pk):
        user_orders = Order.objects.filter(user=pk)
        return render(request, 'app_orders/order_history.html', {'orders': user_orders})


class OnlyOrder(LoginRequiredMixin, View):
    template_name = 'app_order/order_detail.html'

    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        products = OrderItem.objects.select_related('product').filter(order_id=pk)
        return render(request, 'app_orders/order_detail.html', {'order': order, 'products': products})

    def post(self, request, pk):
        Order.objects.filter(pk=pk).update(pay_method=request.POST['order'])
        return redirect("order:payment", pk=pk)
