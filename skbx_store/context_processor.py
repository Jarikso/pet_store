import random
from app_account.forms import PassimLoginForm, CreationUserForm
from app_catalog.models import Product, Category
from app_catalog.filters import ProductFilters
from app_cart.cart import Cart


def get_context_data(request):
    context = {
        'login': PassimLoginForm(),
        'categories': Category.objects.all(),
        'filters': ProductFilters(),
        'cart': Cart(request),
        'hot_item': random.choice(Product.objects.filter(hot_offer=True))
    }
    return context
