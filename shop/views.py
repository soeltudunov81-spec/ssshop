from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests
import json
from .models import Product, Order


def product_list(request):
    products = Product.objects.filter(is_available=True).prefetch_related('images')
    return render(request, 'shop/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product.objects.prefetch_related('images'), pk=pk, is_available=True)
    sizes = product.get_sizes_list()
    return render(request, 'shop/product_detail.html', {'product': product, 'sizes': sizes})


def send_telegram_message(order):
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    
    if not token or not chat_id:
        return False
    
    message = (
        f"🛒 Новый заказ!\n\n"
        f"📦 Товар: {order.product.name}\n"
        f"📏 Размер: {order.size}\n"
        f"💰 Цена: {order.product.price} ₽\n"
        f"👤 Клиент TG: @{order.telegram_username}"
    )
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, data=data, timeout=5)
        return response.status_code == 200
    except requests.exceptions.Timeout:
        return False
    except Exception:
        return False


@csrf_exempt
@require_POST
def create_order(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        size = data.get('size')
        telegram_username = data.get('telegram_username', '').strip().lstrip('@')
        
        if not all([product_id, size, telegram_username]):
            return JsonResponse({'success': False, 'error': 'Заполните все поля'}, status=400)
        
        product = get_object_or_404(Product, pk=product_id, is_available=True)
        
        if size not in product.get_sizes_list():
            return JsonResponse({'success': False, 'error': 'Недоступный размер'}, status=400)
        
        order = Order.objects.create(
            product=product,
            size=size,
            telegram_username=telegram_username
        )
        
        telegram_sent = send_telegram_message(order)
        order.telegram_sent = telegram_sent
        order.save()
        
        return JsonResponse({
            'success': True, 
            'message': 'Заказ успешно создан! Мы свяжемся с вами в Telegram.',
            'order_id': order.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Неверный формат данных'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'Ошибка сервера'}, status=500)
