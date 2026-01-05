# Руководство по развертыванию SS Shop на Railway

Это пошаговая инструкция по развертыванию интернет-магазина SS Shop на платформе Railway.

## Содержание

1. [Подготовка](#подготовка)
2. [Настройка Cloudinary](#настройка-cloudinary)
3. [Настройка Telegram бота](#настройка-telegram-бота)
4. [Развертывание на Railway](#развертывание-на-railway)
5. [Настройка переменных окружения](#настройка-переменных-окружения)
6. [Создание суперпользователя](#создание-суперпользователя)
7. [Использование админ-панели](#использование-админ-панели)

---

## Подготовка

### Требования

- Аккаунт на [Railway](https://railway.app)
- Аккаунт на [Cloudinary](https://cloudinary.com) (бесплатный тариф)
- Telegram бот (создается через [@BotFather](https://t.me/BotFather))
- GitHub аккаунт (для загрузки кода)

---

## Настройка Cloudinary

Cloudinary используется для хранения изображений товаров.

### Шаг 1: Создание аккаунта

1. Перейдите на [cloudinary.com](https://cloudinary.com)
2. Нажмите "Sign Up for Free"
3. Заполните форму регистрации
4. Подтвердите email

### Шаг 2: Получение ключей API

1. Войдите в [Cloudinary Dashboard](https://console.cloudinary.com/console)
2. На главной странице вы увидите:
   - **Cloud Name** - название вашего облака
   - **API Key** - ключ API
   - **API Secret** - секретный ключ API

3. Запишите эти данные, они понадобятся позже:
   ```
   CLOUDINARY_CLOUD_NAME=ваш_cloud_name
   CLOUDINARY_API_KEY=ваш_api_key
   CLOUDINARY_API_SECRET=ваш_api_secret
   ```

---

## Настройка Telegram бота

### Шаг 1: Создание бота

1. Откройте Telegram и найдите [@BotFather](https://t.me/BotFather)
2. Отправьте команду `/newbot`
3. Введите название бота (например: "SS Shop Orders")
4. Введите username бота (например: `ssshop_orders_bot`)
5. Сохраните полученный токен:
   ```
   TELEGRAM_BOT_TOKEN=ваш_токен_бота
   ```

### Шаг 2: Получение Chat ID

1. Напишите что-нибудь вашему боту
2. Перейдите по ссылке: `https://api.telegram.org/botВАШ_ТОКЕН/getUpdates`
3. Найдите в ответе `"chat":{"id":ЧИСЛО}` - это ваш Chat ID
4. Сохраните его:
   ```
   TELEGRAM_CHAT_ID=ваш_chat_id
   ```

---

## Развертывание на Railway

### Шаг 1: Подготовка репозитория

1. Загрузите код на GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/ваш-username/ss-shop.git
   git push -u origin main
   ```

### Шаг 2: Создание проекта на Railway

1. Войдите на [Railway](https://railway.app)
2. Нажмите "New Project"
3. Выберите "Deploy from GitHub repo"
4. Авторизуйте Railway в GitHub и выберите репозиторий

### Шаг 3: Добавление PostgreSQL

1. В проекте нажмите "New"
2. Выберите "Database" → "Add PostgreSQL"
3. Railway автоматически создаст базу данных и переменную `DATABASE_URL`

---

## Настройка переменных окружения

В настройках проекта Railway перейдите в раздел "Variables" и добавьте:

### Обязательные переменные

```
SECRET_KEY=ваш-очень-длинный-случайный-ключ
DEBUG=False
ALLOWED_HOSTS=.railway.app

# Cloudinary
CLOUDINARY_CLOUD_NAME=ваш_cloud_name
CLOUDINARY_API_KEY=ваш_api_key
CLOUDINARY_API_SECRET=ваш_api_secret

# Telegram
TELEGRAM_BOT_TOKEN=ваш_токен_бота
TELEGRAM_CHAT_ID=ваш_chat_id
```

### Генерация SECRET_KEY

Для генерации безопасного ключа выполните в Python:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

---

## Создание суперпользователя

### Через Railway CLI

1. Установите Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```

2. Авторизуйтесь:
   ```bash
   railway login
   ```

3. Подключитесь к проекту:
   ```bash
   railway link
   ```

4. Создайте суперпользователя:
   ```bash
   railway run python manage.py createsuperuser
   ```

### Через веб-консоль Railway

1. В проекте откройте вкладку "Deployments"
2. Нажмите на активный деплоймент
3. Откройте "Shell"
4. Выполните:
   ```bash
   python manage.py createsuperuser
   ```

Введите свои данные для создания учетной записи администратора.

---

## Использование админ-панели

### Вход в админ-панель

1. Перейдите по адресу: `https://ваш-домен.railway.app/admin/`
2. Введите email и пароль суперпользователя

### Управление товарами

1. В разделе "Товары" нажмите "Добавить товар"
2. Заполните поля:
   - **Название** - название товара
   - **Описание** - описание товара
   - **Цена** - цена в рублях
   - **Размеры** - размеры через пробел (например: `S M L XL 38 39 40`)
   - **В наличии** - галочка для отображения на сайте
3. В секции "Изображения товаров" добавьте фотографии
4. Нажмите "Сохранить"

### Управление заказами

1. В разделе "Заказы" вы увидите все заказы
2. Для каждого заказа отображается:
   - Номер заказа
   - Товар и размер
   - Telegram username клиента
   - Статус заказа
   - Отправлено ли уведомление в Telegram
3. Измените статус заказа по необходимости

---

## Устранение неполадок

### Изображения не загружаются

1. Проверьте правильность ключей Cloudinary
2. Убедитесь, что все три переменных заданы:
   - `CLOUDINARY_CLOUD_NAME`
   - `CLOUDINARY_API_KEY`
   - `CLOUDINARY_API_SECRET`

### Уведомления не приходят в Telegram

1. Проверьте токен бота
2. Убедитесь, что Chat ID правильный
3. Напишите что-нибудь боту перед первым заказом
4. Проверьте, что переменные заданы:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`

### Ошибка 500

1. Проверьте логи в Railway (раздел "Deployments")
2. Убедитесь, что все миграции выполнены:
   ```bash
   railway run python manage.py migrate
   ```

### Статические файлы не отображаются

Выполните сбор статических файлов:
```bash
railway run python manage.py collectstatic --noinput
```

---

## Полезные команды

```bash
# Применить миграции
railway run python manage.py migrate

# Собрать статические файлы
railway run python manage.py collectstatic --noinput

# Создать суперпользователя
railway run python manage.py createsuperuser

# Открыть Django shell
railway run python manage.py shell

# Просмотреть логи
railway logs
```

---

## Поддержка

Если у вас возникли вопросы или проблемы:

1. Проверьте логи Railway
2. Убедитесь, что все переменные окружения настроены правильно
3. Проверьте подключение к базе данных PostgreSQL

---

**SS Shop** - Премиальный интернет-магазин
