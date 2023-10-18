from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.http import HttpResponseRedirect

from .models import Category, Product, Review
from .filters import ProductFilters, format_filter

from .forms import CreateReview
from app_cart.form import CartAddProductForm


class MainListView(generic.ListView):
    model = Product
    template_name = 'app_catalog/catalog_offers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chosen_category'] = Category.objects.filter(chosen=True)
        context['hot_offer'] = Product.objects.filter(hot_offer=True)
        context['limited'] = Product.objects.filter(limited_edition=True)
        return context


class AllListView(generic.ListView):
    paginate_by = 8
    model = Product
    template_name = 'app_catalog/catalog.html'

    def get_queryset(self):
        super(AllListView, self).get_queryset()
        data_filter = format_filter(self.request.GET)
        self.request.GET = self.request.GET.copy()
        self.request.GET['price__gt'] = data_filter['min']
        self.request.GET['price__lt'] = data_filter['max']
        qs = ProductFilters(self.request.GET, queryset=Product.objects.all().order_by(data_filter['sorted']))
        if len(data_filter['category']) != 0:
            qs = ProductFilters(self.request.GET, queryset=Product.objects.filter(category_id__in=data_filter['category']).order_by(data_filter['sorted']))
        return qs.qs

    def get_context_data(self):
        context = super().get_context_data()
        get_filter = format_filter(self.request.GET)
        context['data_filter'] = get_filter
        context['url'] = ''.join([f'{key}={get_filter[key]}&' for key in self.request.GET if key in get_filter])
        return context


class ProductDetail(generic.DetailView):
    model = Product
    template_name = 'app_catalog/catalog_product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context['cart_product_form'] = CartAddProductForm()
        context['form'] = CreateReview()
        context['reviews'] = Review.objects.filter(product_id=product.id)
        return context

    def post(self, request, slug):
        product = Product.objects.get(slug=slug)
        form = CreateReview(request.POST)
        if form.is_valid():
            create_review = form.save(commit=False)
            create_review.product_id = product.id
            create_review.save()
            return HttpResponseRedirect(reverse('catalog:goods', args=[slug]))
        return render(request, 'app_catalog/catalog_product.html', context={'product': product, 'form': form})
