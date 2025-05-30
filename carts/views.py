from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from store.models import Variation, Product
from django.core.exceptions import ObjectDoesNotExist


# Helper function to get or create cart_id from session
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_variations = []

    if request.method == "POST":
        for key in request.POST:
            value = request.POST[key]
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variations.append(variation)
            except Variation.DoesNotExist:
                pass

    cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(product=product, cart=cart)

    existing_item = None
    for item in cart_items:
        item_variations = item.variations.all()
        if set(item_variations) == set(product_variations):
            existing_item = item
            break

    if existing_item:
        existing_item.quantity += 1
        existing_item.save()
    else:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        if product_variations:
            cart_item.variations.set(product_variations)
        cart_item.save()

    return redirect('cart')



def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))

    try:
        cart_item = CartItem.objects.filter(product=product, cart=cart, id=cart_item_id).first()
        if cart_item and cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        elif cart_item:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass

    return redirect('cart')


# Remove product from cart with specific variations
def remove_cart_item(request, product_id, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, product_id=product_id, cart__cart_id=_cart_id(request))
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart')



def cart(request, total=0, quantity=0, cart_items=0):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        tax = (9 * total) / 100  
        grand_total = total + tax
    except ObjectDoesNotExist:
        cart_items = []
        total = 0
        quantity = 0
        tax = 0
        grand_total = 0

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'tax': round(tax, 2),
        'grand_total': round(grand_total, 2),
    }
    return render(request, 'store/cart.html', context)
