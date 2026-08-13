from decimal import Decimal

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Product


def home(request):
    products = Product.objects.all()[:4]
    return render(request, 'store/home.html', {'products': products})


def products(request):
    products = Product.objects.all()
    return render(request, 'store/products.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})


def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        price = request.POST.get('price', '0').strip()
        stock = request.POST.get('stock', '0').strip()
        image = request.FILES.get('image')

        if not name or not price:
            messages.error(request, 'Product name and price are required.')
            return render(request, 'store/create_product.html', {
                'name': name,
                'description': description,
                'price': price,
                'stock': stock,
            })

        try:
            price_value = Decimal(price)
        except Exception:
            messages.error(request, 'Enter a valid price.')
            return render(request, 'store/create_product.html', {
                'name': name,
                'description': description,
                'price': price,
                'stock': stock,
            })

        try:
            stock_value = int(stock)
        except Exception:
            stock_value = 0

        Product.objects.create(
            name=name,
            description=description,
            price=price_value,
            stock=max(stock_value, 0),
            image=image,
        )
        messages.success(request, 'Product created successfully.')
        return redirect('products')

    return render(request, 'store/create_product.html')


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        price = request.POST.get('price', '0').strip()
        stock = request.POST.get('stock', '0').strip()
        image = request.FILES.get('image')

        if not name or not price:
            messages.error(request, 'Product name and price are required.')
            return render(request, 'store/edit_product.html', {
                'product': product,
                'name': name,
                'description': description,
                'price': price,
                'stock': stock,
            })

        try:
            price_value = Decimal(price)
        except Exception:
            messages.error(request, 'Enter a valid price.')
            return render(request, 'store/edit_product.html', {
                'product': product,
                'name': name,
                'description': description,
                'price': price,
                'stock': stock,
            })

        try:
            stock_value = int(stock)
        except Exception:
            stock_value = 0

        product.name = name
        product.description = description
        product.price = price_value
        product.stock = max(stock_value, 0)
        if image:
            product.image = image
        product.save()

        messages.success(request, 'Product updated successfully.')
        return redirect('products')

    return render(request, 'store/edit_product.html', {'product': product})


@require_POST
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully.')
    return redirect('products')


def _get_cart(request):
    return request.session.get('cart', {})


def _save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request)
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    _save_cart(request, cart)
    messages.success(request, f"Added {product.name} to your cart.")
    return redirect(request.META.get('HTTP_REFERER', 'products'))


@require_POST
def remove_from_cart(request, product_id):
    cart = _get_cart(request)
    if str(product_id) in cart:
        del cart[str(product_id)]
        _save_cart(request, cart)
        messages.success(request, "Item removed from your cart.")
    return redirect('cart')


def cart(request):
    cart_data = _get_cart(request)
    items = []
    total = Decimal('0.00')
    if cart_data:
        product_ids = [int(k) for k in cart_data.keys() if str(k).isdigit()]
        products = Product.objects.filter(pk__in=product_ids) if product_ids else []
        for product in products:
            try:
                quantity = int(cart_data.get(str(product.id), 0))
            except (TypeError, ValueError):
                quantity = 0
            if quantity <= 0:
                continue
            subtotal = product.price * quantity
            total += subtotal
            items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })
    return render(request, 'store/cart.html', {'items': items, 'total': total})


def checkout(request):
    cart_data = _get_cart(request)
    items = []
    total = Decimal('0.00')
    if cart_data:
        product_ids = [int(k) for k in cart_data.keys() if str(k).isdigit()]
        products = Product.objects.filter(pk__in=product_ids) if product_ids else []
        for product in products:
            try:
                quantity = int(cart_data.get(str(product.id), 0))
            except (TypeError, ValueError):
                quantity = 0
            if quantity <= 0:
                continue
            subtotal = product.price * quantity
            total += subtotal
            items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        payment_method = request.POST.get('payment_method', '').strip()

        if not all([full_name, email, phone, address, payment_method]):
            messages.error(request, 'Please fill in all fields and select a payment method.')
        elif not items:
            messages.error(request, 'Your cart is empty.')
        else:
            request.session['cart'] = {}
            request.session.modified = True
            messages.success(request, f'Order placed successfully via {payment_method}. We will contact you shortly.')
            return redirect('products')

    return render(request, 'store/checkout.html', {'items': items, 'total': total})


def bookings(request):
    return render(request, 'store/bookings.html')


def booking_detail(request, booking_id):
    return render(request, 'store/booking_detail.html', {'booking_id': booking_id})


def contact(request):
    return render(request, 'store/contact.html')
