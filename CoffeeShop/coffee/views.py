from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Coffee, Order, Contact

def is_staff(user):
    return user.is_staff

def home(request):
    coffee = Coffee.objects.all()
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    cart_items = []
    for coffee_id, quantity in cart.items():
        coffee_item = get_object_or_404(Coffee, id=int(coffee_id))
        subtotal = coffee_item.price * quantity
        cart_items.append({'coffee': coffee_item, 'quantity': quantity, 'subtotal': subtotal})
    return render(request, 'home.html', {'coffee': coffee, 'cart_count': cart_count, 'cart_items': cart_items})

@login_required
def add_to_cart(request, coffee_id):
    coffee = get_object_or_404(Coffee, id=coffee_id)
    cart = request.session.get('cart', {})
    cart[str(coffee_id)] = cart.get(str(coffee_id), 0) + 1
    request.session['cart'] = cart
    messages.success(request, f'{coffee.name} has been added to your cart!')
    return redirect('home')

def cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for coffee_id, quantity in cart.items():
        coffee = get_object_or_404(Coffee, id=int(coffee_id))
        subtotal = coffee.price * quantity
        total += subtotal
        items.append({'coffee': coffee, 'quantity': quantity, 'subtotal': subtotal})
    cart_count = sum(cart.values())
    return render(request, 'cart.html', {'items': items, 'total': total, 'cart_count': cart_count, 'cart_items': items})

def search(request):
    query = request.GET.get('q', '')
    if query:
        coffee = Coffee.objects.filter(name__icontains=query) | Coffee.objects.filter(description__icontains=query)
    else:
        coffee = Coffee.objects.all()
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    cart_items = []
    for coffee_id, quantity in cart.items():
        coffee_item = get_object_or_404(Coffee, id=int(coffee_id))
        subtotal = coffee_item.price * quantity
        cart_items.append({'coffee': coffee_item, 'quantity': quantity, 'subtotal': subtotal})
    return render(request, 'home.html', {'coffee': coffee, 'query': query, 'cart_count': cart_count, 'cart_items': cart_items})

def coffee_detail(request, coffee_id):
    coffee = get_object_or_404(Coffee, id=coffee_id)
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    cart_items = []
    for c_id, quantity in cart.items():
        coffee_item = get_object_or_404(Coffee, id=int(c_id))
        subtotal = coffee_item.price * quantity
        cart_items.append({'coffee': coffee_item, 'quantity': quantity, 'subtotal': subtotal})
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart[str(coffee_id)] = cart.get(str(coffee_id), 0) + quantity
        request.session['cart'] = cart
        messages.success(request, f'{quantity} x {coffee.name} has been added to your cart!')
        return redirect('cart')
    return render(request, 'coffee_detail.html', {'coffee': coffee, 'cart_count': cart_count, 'cart_items': cart_items})

def about(request):
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    cart_items = []
    for coffee_id, quantity in cart.items():
        coffee_item = get_object_or_404(Coffee, id=int(coffee_id))
        subtotal = coffee_item.price * quantity
        cart_items.append({'coffee': coffee_item, 'quantity': quantity, 'subtotal': subtotal})
    return render(request, 'about.html', {'cart_count': cart_count, 'cart_items': cart_items})

def contact(request):
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    cart_items = []
    for coffee_id, quantity in cart.items():
        coffee_item = get_object_or_404(Coffee, id=int(coffee_id))
        subtotal = coffee_item.price * quantity
        cart_items.append({'coffee': coffee_item, 'quantity': quantity, 'subtotal': subtotal})
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        Contact.objects.create(name=name, email=email, message=message)
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')
    return render(request, 'contact.html', {'cart_count': cart_count, 'cart_items': cart_items})

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for coffee_id, quantity in cart.items():
        coffee = get_object_or_404(Coffee, id=int(coffee_id))
        subtotal = coffee.price * quantity
        total += subtotal
        items.append({'coffee': coffee, 'quantity': quantity, 'subtotal': subtotal})
    cart_count = sum(cart.values())
    if request.method == 'POST':
        # Save order to database
        serializable_items = []
        for item in items:
            coffee = item['coffee']
            serializable_items.append({
                'coffee': {
                    'id': coffee.id,
                    'name': coffee.name,
                    'price': float(coffee.price),
                    'image': coffee.image.url if coffee.image else None,
                    'description': coffee.description
                },
                'quantity': item['quantity'],
                'subtotal': float(item['subtotal'])
            })
        order = Order.objects.create(user=request.user, items=serializable_items, total=total)
        request.session['order_id'] = order.id
        return redirect('payment')
    return render(request, 'checkout.html', {'items': items, 'total': total, 'cart_count': cart_count, 'cart_items': items})

@login_required
@user_passes_test(lambda u: not u.is_staff, login_url='admin_dashboard')
def payment(request):
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('home')
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items
    total = order.total
    cart_count = sum(request.session.get('cart', {}).values())
    cart_items = []
    for coffee_id, quantity in request.session.get('cart', {}).items():
        coffee_item = get_object_or_404(Coffee, id=int(coffee_id))
        subtotal = coffee_item.price * quantity
        cart_items.append({'coffee': coffee_item, 'quantity': quantity, 'subtotal': subtotal})
    if request.method == 'POST':
        # Handle payment screenshot upload
        payment_screenshot = request.FILES.get('payment_screenshot')
        if payment_screenshot:
            # Here you would save the screenshot and process the payment
            # For now, just clear the cart and order
            request.session['cart'] = {}
            del request.session['order_id']
            messages.success(request, 'Payment confirmed! Your order has been placed successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Please upload a payment screenshot.')
    return render(request, 'payment.html', {'items': items, 'total': total, 'cart_count': cart_count, 'cart_items': cart_items})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
@user_passes_test(is_staff)
def admin_dashboard(request):
    total_coffees = Coffee.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    total_contacts = Contact.objects.count()
    recent_orders = Order.objects.all().order_by('-created_at')[:5]
    return render(request, 'admin_dashboard.html', {
        'total_coffees': total_coffees,
        'pending_orders': pending_orders,
        'total_contacts': total_contacts,
        'recent_orders': recent_orders,
    })

@login_required
@user_passes_test(is_staff)
def manage_coffee(request):
    coffees = Coffee.objects.all()
    if request.method == 'POST':
        for coffee in coffees:
            quantity = request.POST.get(f'quantity_{coffee.id}')
            price = request.POST.get(f'price_{coffee.id}')
            if quantity:
                coffee.quantity = int(quantity)
            if price:
                coffee.price = float(price)
            coffee.save()
        messages.success(request, 'Coffee inventory updated successfully.')
        return redirect('manage_coffee')
    return render(request, 'manage_coffee.html', {'coffees': coffees})

@login_required
@user_passes_test(is_staff)
def confirm_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'confirmed'
    order.save()
    messages.success(request, f'Order {order.id} confirmed.')
    return redirect('view_orders')

@login_required
@user_passes_test(is_staff)
def view_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'view_orders.html', {'orders': orders})

@login_required
@user_passes_test(is_staff)
def view_contacts(request):
    contacts = Contact.objects.all().order_by('-created_at')
    return render(request, 'view_contacts.html', {'contacts': contacts})
