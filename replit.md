# SS Shop - E-commerce Platform

## Project Overview

SS Shop is a premium e-commerce website built with Django, featuring:

- **Frontend**: Tailwind CSS with glassmorphism design effects
- **Backend**: Django 5.2 with PostgreSQL database
- **Media Storage**: Cloudinary for image hosting
- **Notifications**: Telegram bot integration for order notifications
- **Admin Panel**: Full CRUD operations for products and orders

## Project Structure

```
/
├── ssshop/                 # Django project settings
│   ├── settings.py        # Main configuration
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI configuration
├── shop/                   # Main application
│   ├── models.py          # Product, ProductImage, Order models
│   ├── views.py           # Views for catalog and orders
│   ├── admin.py           # Admin panel customization
│   └── urls.py            # App URL routing
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   └── shop/              # Shop templates
│       ├── product_list.html    # Product catalog
│       └── product_detail.html  # Product detail page
├── static/                 # Static files
├── staticfiles/            # Collected static files
├── Procfile               # Railway deployment config
├── runtime.txt            # Python version
└── RAILWAY_DEPLOYMENT_GUIDE.md  # Deployment guide (Russian)
```

## Environment Variables

Required environment variables:

- `PGDATABASE`, `PGUSER`, `PGPASSWORD`, `PGHOST`, `PGPORT` - PostgreSQL connection
- `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` - Cloudinary for images
- `TELEGRAM_BOT_TOKEN` - Telegram bot token for notifications
- `TELEGRAM_CHAT_ID` - Chat ID for receiving order notifications
- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)

## Key Features

1. **Product Catalog**: Grid layout with glassmorphism cards
2. **Product Detail**: Image gallery with thumbnails, size selection
3. **Order System**: No registration required, just Telegram username
4. **Telegram Notifications**: Automatic order notifications (5 sec timeout)
5. **Admin Panel**: Easy product management with inline image uploads

## Admin Credentials

Admin credentials are configured during deployment. Use `python manage.py createsuperuser` to create your admin account.

## Running the Project

The project runs on port 5000 using Django's development server:

```bash
python manage.py runserver 0.0.0.0:5000
```

For production (Railway):

```bash
gunicorn ssshop.wsgi:application --bind 0.0.0.0:$PORT
```

## Design

- **Color Scheme**: White background (#FFFFFF), Black text (#000000)
- **Effects**: Glassmorphism with backdrop-filter blur
- **Typography**: Inter font family
- **Responsive**: Mobile-first design with Tailwind CSS

## User Preferences

- Russian language interface
- Premium, high-contrast design aesthetic
- Simple ordering without registration
- Telegram as primary communication channel
