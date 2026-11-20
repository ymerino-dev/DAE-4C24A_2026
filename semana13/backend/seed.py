"""Seed the database with sample categories, products, and PNG images."""

import os
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django  # noqa: E402
from django.conf import settings  # noqa: E402
from django.utils.text import slugify  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

django.setup()

from catalog.models import Category, Product  # noqa: E402


IMAGE_SIZE = (640, 480)

CATEGORIES = [
    {
        'name': 'Electronics',
        'description': 'Devices and gadgets for everyday use.',
        'color': (37, 99, 235),
    },
    {
        'name': 'Clothing',
        'description': 'Apparel and accessories for all seasons.',
        'color': (124, 58, 237),
    },
    {
        'name': 'Home & Kitchen',
        'description': 'Practical items for a comfortable home.',
        'color': (15, 118, 110),
    },
]

PRODUCTS = [
    {
        'name': 'Wireless Headphones',
        'category': 'Electronics',
        'description': 'Over-ear headphones with active noise cancellation.',
        'price': '89.90',
        'stock': 12,
    },
    {
        'name': 'Bluetooth Speaker',
        'category': 'Electronics',
        'description': 'Portable speaker with rich stereo sound.',
        'price': '59.50',
        'stock': 20,
    },
    {
        'name': 'Smart Watch',
        'category': 'Electronics',
        'description': 'Fitness tracker with heart rate and sleep monitoring.',
        'price': '129.00',
        'stock': 8,
    },
    {
        'name': 'USB-C Charger',
        'category': 'Electronics',
        'description': 'Fast 65W charger with two USB-C ports.',
        'price': '24.99',
        'stock': 35,
    },
    {
        'name': 'Cotton T-Shirt',
        'category': 'Clothing',
        'description': 'Soft cotton t-shirt with a regular fit.',
        'price': '18.50',
        'stock': 40,
    },
    {
        'name': 'Denim Jacket',
        'category': 'Clothing',
        'description': 'Classic blue denim jacket for cool evenings.',
        'price': '64.00',
        'stock': 15,
    },
    {
        'name': 'Ceramic Mug',
        'category': 'Home & Kitchen',
        'description': 'Handmade ceramic mug for coffee and tea.',
        'price': '12.75',
        'stock': 28,
    },
    {
        'name': 'Stainless Steel Pan',
        'category': 'Home & Kitchen',
        'description': 'Durable non-stick pan for everyday cooking.',
        'price': '45.90',
        'stock': 10,
    },
]


def generate_product_image(product, color):
    """Create a real PNG sample image and return its relative Media path."""
    image_dir = Path(settings.MEDIA_ROOT) / 'products'
    image_dir.mkdir(parents=True, exist_ok=True)

    filename = f'{slugify(product["name"])}.png'
    image_path = image_dir / filename

    image = Image.new('RGB', IMAGE_SIZE, color)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    draw.rectangle(
        (20, 20, IMAGE_SIZE[0] - 20, IMAGE_SIZE[1] - 20),
        outline=(255, 255, 255),
        width=4,
    )
    draw.text((40, 60), product['name'], fill=(255, 255, 255), font=font)
    draw.text(
        (40, 100),
        f'Category: {product["category"]}',
        fill=(255, 255, 255),
        font=font,
    )
    draw.text(
        (40, 140),
        f'Price: ${product["price"]}',
        fill=(255, 255, 255),
        font=font,
    )
    image.save(image_path, format='PNG')

    return f'products/{filename}'


def seed_data():
    """Insert exactly the configured categories and products."""
    category_names = [item['name'] for item in CATEGORIES]
    product_names = [item['name'] for item in PRODUCTS]

    Category.objects.exclude(name__in=category_names).delete()
    Product.objects.exclude(name__in=product_names).delete()

    categories = {}
    for category_data in CATEGORIES:
        category, _ = Category.objects.update_or_create(
            name=category_data['name'],
            defaults={'description': category_data['description']},
        )
        categories[category_data['name']] = (
            category,
            category_data['color'],
        )

    for product_data in PRODUCTS:
        category, color = categories[product_data['category']]
        image_path = generate_product_image(product_data, color)

        Product.objects.update_or_create(
            name=product_data['name'],
            defaults={
                'category': category,
                'description': product_data['description'],
                'price': product_data['price'],
                'stock': product_data['stock'],
                'image': image_path,
            },
        )

    print(f'Categories seeded: {Category.objects.count()}')
    print(f'Products seeded: {Product.objects.count()}')


if __name__ == '__main__':
    seed_data()
