from django.db import models
from cloudinary.models import CloudinaryField


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    sizes = models.CharField(max_length=255, verbose_name='Размеры', 
                            help_text='Введите размеры через пробел (например: S M L XL 38 39 40)')
    is_available = models.BooleanField(default=True, verbose_name='В наличии')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_sizes_list(self):
        return self.sizes.split() if self.sizes else []

    def get_main_image(self):
        first_image = self.images.first()
        return first_image.image.url if first_image else None


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                                related_name='images', verbose_name='Товар')
    image = CloudinaryField('image')
    is_main = models.BooleanField(default=False, verbose_name='Главное изображение')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'
        ordering = ['order', 'id']

    def __str__(self):
        return f'Изображение для {self.product.name}'


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                                related_name='orders', verbose_name='Товар')
    size = models.CharField(max_length=50, verbose_name='Размер')
    telegram_username = models.CharField(max_length=255, verbose_name='Telegram username')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, 
                             default='new', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    telegram_sent = models.BooleanField(default=False, verbose_name='Отправлено в Telegram')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ #{self.id} - {self.product.name} ({self.size})'
