from django.shortcuts import render, get_object_or_404
from store.models import Product, Category

def store(request, category_slug=None):
    products = None

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
    else:
        products = Product.objects.filter(is_available=True)

    product_count = products.count()
    context = {
        "products": products,
        "product_count": product_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, category=category, slug=product_slug, is_available=True)

    context = {
        'product': product
    }
    return render(request, 'store/product_detail.html', context)


