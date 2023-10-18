from django import forms

from django.contrib.admin import ModelAdmin
from django_filters import CharFilter

from .models import Product, Category
import django_filters


class ProductFilters(django_filters.FilterSet):
    available = CharFilter(method='my_available')
    delivery = CharFilter(method='my_delivery')
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['available']

    def my_available(self, querset, name, value):
        return querset.filter(available=True)

    def my_delivery(self, querset, name, value):
        return querset.filter(price__gte=2000)


def format_filter(request_dict):
    category = Category.objects.all()
    dict_slug = {cat.slug: cat.id for cat in category}
    format_data = {key: value for key, value in request_dict.items()}
    format_data['sorted'] = request_dict['sorted'] if 'sorted' in request_dict else 'name'
    format_data['page'] = request_dict['page'] if 'page' in request_dict else 1
    format_data['price'] = request_dict['price'].replace(';', '%3B') if 'price' in request_dict else ''
    format_data['min'] = request_dict['price'].split(';')[0] if 'price' in request_dict else 0
    format_data['max'] = request_dict['price'].split(';')[1] if 'price' in request_dict else 300000
    format_data['category'] = []
    for key in format_data:
        if key in dict_slug:
            format_data['category'].append(dict_slug[key])
    return format_data

# def get_format_filter(request_dict):
#     pass
