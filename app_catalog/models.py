from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='название')
    slug = models.SlugField(max_length=200, db_index=True, unique=True, verbose_name='ссылка')
    chosen = models.BooleanField(default=False, verbose_name='избранная категория')
    category_icon = models.ImageField(upload_to='icon_category/', blank=True, verbose_name='иконка')
    category_img = models.ImageField(upload_to='img_category/', blank=True, verbose_name='изображение')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/catalog/?{self.slug}=on#'


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.PROTECT, verbose_name='категория')
    name = models.CharField(max_length=200, db_index=True, verbose_name='название')
    slug = models.SlugField(max_length=200, db_index=True, verbose_name='ссылка')
    description = models.TextField(blank=True, verbose_name='описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена')
    available = models.BooleanField(default=True, verbose_name='наличие')
    hot_offer = models.BooleanField(default=False, verbose_name='горячее предложение')
    limited_edition = models.BooleanField(default=False, verbose_name='ограниченный тираж')
    reviews = models.PositiveIntegerField(default=0, verbose_name='количество отзывов')
    bought = models.PositiveIntegerField(default=0, verbose_name='куплено')
    date_create = models.DateTimeField(verbose_name='дата создания')  # добавить auto_now_add

    class Meta:
        ordering = ('id',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='review', on_delete=models.PROTECT, verbose_name='товар')
    full_name = models.CharField(max_length=50, db_index=True, blank=True, verbose_name='полное имя')
    description = models.TextField(max_length=200, verbose_name='отзыв')
    email = models.EmailField(max_length=50, blank=True, verbose_name='электронная почта')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.description

    def delete(self, *args, **kwargs):
        Product.objects.filter(id=self.product.id).update(
            reviews=len(Review.objects.filter(product_id=self.product.id)) - 1)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        Product.objects.filter(id=self.product.id).update(
            reviews=len(Review.objects.filter(product_id=self.product.id)) + 1)
        super().save(*args, **kwargs)


class Properties(models.Model):
    product = models.ForeignKey(Product, related_name='properties', on_delete=models.PROTECT, verbose_name='товар')
    title = models.CharField(max_length=40, db_index=True, blank=True, verbose_name='Характеристика')
    description = models.CharField(max_length=30, verbose_name='Описание')

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'

    def __str__(self):
        return self.title


class Image(models.Model):
    product = models.ForeignKey(Product, related_name='image', on_delete=models.PROTECT, verbose_name='товар')
    image = models.ImageField(upload_to='img_product/', blank=True, verbose_name='изображение')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
