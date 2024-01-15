from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import (Product, News, StockHistory,
                     Cart, CartItem,Order)
from .forms import ProductForm, InventoryForm, Inventory,StockAdjustmentForm,CheckoutForm,UserProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.core.mail import send_mail
from django.conf import settings

def product_views(request):
    return render(request, 'product_views.html')

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully.')
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'create_product.html', {'form': form})

@user_passes_test(is_admin)
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Assuming you have a view named 'product_list'
    else:
        form = ProductForm(instance=product)

    return render(request, 'update_product.html', {'form': form})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

@user_passes_test(is_admin)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')  # Assuming you have a view named 'product_list'
    
    return render(request, 'delete_product.html', {'product': product})

def search_products(request):
    query = request.GET.get('q', '')
    
    if query:
        products = Product.objects.filter(title__icontains=query)
    else:
        products = Product.objects.all()

    return render(request, 'search_products.html', {'products': products, 'query': query})


def product_views(request):
    products = Product.objects.all()
    return render(request, 'product_views.html', {'products': products})

@user_passes_test(is_admin)
def inventory_list(request):
    inventory_items = Inventory.objects.all()
    total = sum(item.subtotal or 0 for item in inventory_items)
    return render(request, 'inventory_list.html', {'inventory_items': inventory_items, 'total': total})

@user_passes_test(is_admin)
def add_to_inventory(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            subtotal = product.price * quantity

            # Get or create Inventory object
            inventory_item, created = Inventory.objects.get_or_create(product=product, defaults={'quantity': quantity, 'subtotal': subtotal})

            if not created:
                # If the product is already in inventory, update the quantity and recalculate the subtotal
                inventory_item.quantity += quantity
                inventory_item.subtotal = product.price * inventory_item.quantity
                inventory_item.save()

            # Update the stock level
            inventory_item.stock = inventory_item.quantity
            inventory_item.save()

            return redirect('inventory_list')
    else:
        form = InventoryForm()

    return render(request, 'add_to_inventory.html', {'form': form, 'product': product})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def calculator(request):
    result = None

    if request.method == 'POST':
        # Handle form submission
        num1 = float(request.POST.get('num1', 0))
        num2 = float(request.POST.get('num2', 0))
        operator = request.POST.get('operator', '+')

        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 != 0:
                result = num1 / num2
            else:
                result = 'Cannot divide by zero'

    return render(request, 'calculator.html', {'result': result})

def news_list(request):
    news_articles = News.objects.all().order_by('-created_at')
    return render(request, 'news_list.html', {'news_articles': news_articles})
@user_passes_test(is_admin)
def current_stock(request):
    products_with_stock = Product.objects.filter(inventory__isnull=False).distinct()
    return render(request, 'current_stock.html', {'products_with_stock': products_with_stock})

@user_passes_test(is_admin)
def adjust_stock(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    inventory_item = get_object_or_404(Inventory, product=product)

    if request.method == 'POST':
        form = StockAdjustmentForm(request.POST)
        if form.is_valid():
            adjustment = form.cleaned_data['adjustment']
            inventory_item.quantity += adjustment
            inventory_item.save()

            # Record the stock adjustment in StockHistory
            StockHistory.objects.create(product=product, user=request.user, adjustment=adjustment)

            messages.success(request, 'Stock adjusted successfully.')
            return redirect('current_stock')
    else:
        form = StockAdjustmentForm()

    return render(request, 'adjust_stock.html', {'form': form, 'product': product})
@user_passes_test(is_admin)
def stock_history(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    stock_history_entries = StockHistory.objects.filter(product=product).order_by('-timestamp')
    return render(request, 'stock_history.html', {'product': product, 'stock_history_entries': stock_history_entries})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if the product is already in the cart
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    # If the item is already in the cart, increase the quantity
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"{product.title} added to your cart.")
    return redirect('cart_view')

def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart_view.html', {'cart': cart, 'cart_items': cart_items})

def update_cart(request, cart_item_id, action):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id, cart__user=request.user)

    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            cart_item.delete()

    cart_item.save()
    return redirect('cart_view')


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart_view')


@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Get user information from the form
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            whatsapp_number = form.cleaned_data['whatsapp_number']

            # Prepare email content
            email_subject = 'Checkout Information'
            email_message = f"Customer Information:\nFull Name: {full_name}\nEmail: {email}\nAddress: {address}\nWhatsApp Number: {whatsapp_number}\n\nCart Items:\n"
            for item in cart_items:
                email_message += f"{item.product.title} - Quantity: {item.quantity}\n"

            # Send email with the user's email as the sender
            send_mail(
                email_subject,
                email_message,
                email,  # Use the customer's email as the sender
                [settings.YOUR_EMAIL_ADDRESS],
                fail_silently=False,  # Set to True to suppress exceptions for testing purposes
            )

            # Clear the cart after checkout
            cart_items.delete()
            return redirect('thank_you')  # Redirect to a success page after checkout

    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {'form': form, 'cart_items': cart_items})


def thank_you(request):
    return render(request, 'thank_you.html')

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')  # Redirect to your desired page after registration
    else:
        form = UserCreationForm()
    return render(request, 'register_user.html', {'form': form})



def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to the user profile page after login
            return redirect('user_profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login_user.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('product_list')  


def password_reset_request(request):
    return PasswordResetView.as_view(template_name='password_reset_request.html')(request)

def password_reset_confirm(request, uidb64, token):
    return PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html')(request, uidb64=uidb64, token=token)


@login_required
def user_profile(request):
    user = request.user
    cart_items = CartItem.objects.filter(cart__user=user)
    orders = Order.objects.filter(user=user)

    return render(request, 'user_profile.html', {'user': user, 'cart_items': cart_items, 'orders': orders})

@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'edit_profile.html', {'form': form})


# ====================payment integration=================== 
