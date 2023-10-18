from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from app_catalog.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()


class Order(models.Model):
    number_order = models.CharField(max_length=5, unique=True, verbose_name='номер заказа')
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, verbose_name='пользователь')
    full_name = models.CharField(max_length=50, db_index=True, blank=True, verbose_name='полное имя')
    email = models.EmailField(max_length=50, blank=True, verbose_name='электронная почта')
    phone = PhoneNumberField(null=True, unique=False, blank=True, verbose_name='телефон')
    delivery = models.CharField(max_length=2, blank=True, verbose_name='доставка')
    city = models.CharField(max_length=25, blank=True, verbose_name='город')
    address = models.CharField(max_length=50, blank=True, verbose_name='адрес')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена')
    pay_method = models.CharField(max_length=2, blank=True, verbose_name='способ оплаты')
    paid = models.BooleanField(default=False, verbose_name='статус оплаты')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def save(self, *args, **kwargs):
        count = str(len(Order.objects.all()))
        self.number_order = '2' * (5 - len(count)) + count
        if self.delivery == 'OR' and self.price < 2000:
            self.price += 200
        elif self.delivery == 'EX':
            self.price += 500
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='заказ', related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='', related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1, verbose_name='количество')

    def get_cost(self):
        return self.price * self.quantity

    def get_price(self):
        return self.product.price

    def save(self, *args, **kwargs):
        self.price = self.product.price
        super().save(*args, **kwargs)
        item = OrderItem.objects.filter(product_id=self.product.id)
        Product.objects.filter(id=self.product.id).update(bought=sum([i.quantity for i in item]))

