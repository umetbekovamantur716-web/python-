from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()


class Category(MPTTModel):
    name = models.CharField(max_length=150, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="слизень")
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE, related_name='children',
        null=True, blank=True, verbose_name="Родитель"
    )
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta: 
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

class Brand(models.Model):
    name = models.CharField(max_length=150,verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="слизень")
    logo = models.ImageField(upload_to='brand/', null=True, blank=True) 

    def __str__(self):
        return self.name
    
    class Meta: 
        verbose_name = 'бренд'
        verbose_name_plural = 'Бренды'
    

class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products'
    )
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products'
    )
    name = models.CharField(max_length=150,verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="слизень")
    description = models.TextField(verbose_name="описание")
    price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="цена")
    stock = models.PositiveIntegerField(default=0, verbose_name="Количество товара на складе")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta: 
        verbose_name = 'товар'
        verbose_name_plural = 'Товары'


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='iproduct/')
    is_main = models.BooleanField(default=False, verbose_name="Главная картина")

    def __str__(self):
        return self.product.name 

    class Meta: 
        verbose_name = 'фото товара'
        verbose_name_plural = 'Фотки товаров'

class Attribute(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta: 
        verbose_name = 'атрибут'
        verbose_name_plural = 'Атрибуты'

class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta: 
        verbose_name = 'значение атрибута'
        verbose_name_plural = 'Значения атрибутов'
    
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    attributes = models.ManyToManyField(AttributeValue)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=1)
    sku = models.CharField(unique=True, verbose_name="Артикул", max_length=255)

    def __str__(self):
        return f"{self.product.name} {self.sku}"
    
    class Meta: 
        verbose_name = 'вариант товара'
        verbose_name_plural = 'Варианты товаров'

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} {self.rating}"
    
    class Meta: 
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'