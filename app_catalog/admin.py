from django.contrib import admin
from .models import Category, Product, Review, Properties, Image


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'chosen']
    list_editable = ['chosen']
    prepopulated_fields = {'slug': ('name',)}


class PropertiesAdmin(admin.TabularInline):
    model = Properties
    extra = 3


class ImageAdmin(admin.TabularInline):
    model = Image
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'available', 'hot_offer', 'limited_edition']
    list_filter = ['available']
    list_editable = ['price', 'available', 'hot_offer', 'limited_edition']
    prepopulated_fields = {'slug': ('name',)}
    inlines = (PropertiesAdmin, ImageAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'description']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
