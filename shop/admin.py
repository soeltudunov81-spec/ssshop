from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductImage, Order


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ['image', 'is_main', 'order', 'image_preview']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 80px; max-width: 80px; object-fit: cover;"/>', obj.image.url)
        return '-'
    image_preview.short_description = 'Превью'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'sizes', 'is_available', 'image_preview', 'created_at']
    list_filter = ['is_available', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_available']
    inlines = [ProductImageInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'price')
        }),
        ('Размеры и наличие', {
            'fields': ('sizes', 'is_available'),
            'description': 'Введите размеры через пробел (например: S M L XL 38 39 40)'
        }),
    )

    def image_preview(self, obj):
        main_image = obj.get_main_image()
        if main_image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; object-fit: cover; border-radius: 5px;"/>', main_image)
        return '-'
    image_preview.short_description = 'Фото'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'size', 'telegram_username', 'status', 'telegram_sent', 'created_at']
    list_filter = ['status', 'telegram_sent', 'created_at']
    search_fields = ['product__name', 'telegram_username']
    list_editable = ['status']
    readonly_fields = ['product', 'size', 'telegram_username', 'created_at', 'telegram_sent']
    
    fieldsets = (
        ('Информация о заказе', {
            'fields': ('product', 'size', 'telegram_username')
        }),
        ('Статус', {
            'fields': ('status', 'telegram_sent')
        }),
        ('Даты', {
            'fields': ('created_at',)
        }),
    )


admin.site.site_header = 'SS Shop - Панель управления'
admin.site.site_title = 'SS Shop Admin'
admin.site.index_title = 'Управление магазином'
