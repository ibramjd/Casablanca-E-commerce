from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm
from django.http import JsonResponse
import json

from .models import *

def store_view(request):
    category = request.GET.get('category')
    price = request.GET.get('price')

    products = Product.objects.all()
    if category:
        products = products.filter(category=category)
    if price:
        if price == 'low':
            products = products.filter(price__lt=10.000)
        elif price == 'mid':
            products = products.filter(price__gte=10.000, price__lt=25.000)
        elif price == 'high':
            products = products.filter(price__gte=25.000)

    # Clothes Categories
    men_products = products.filter(category='men')
    women_products = products.filter(category='women')
    kids_products = products.filter(category='kids')

    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(
            user = request.user,
            defaults={'name': request.user.username,}
        )
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_items': 0,
            'get_cart_total': 0,
            'shipping': False,
        }

    context = {
        'men_products':men_products,
        'women_products':women_products,
        'kids_products' :kids_products,
        'items':items,
        'order':order,
        }
    return render(request, 'store/store.html', context)

@login_required(login_url='login')
def cart_view(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(
            user=request.user,
            defaults={'name': request.user.username,}
        )
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_items': 0,
            'get_cart_total': 0,
            'shipping': False,
        }

    context = {
        'items':items,
        'order':order,
        }
    return render(request, 'store/cart.html', context)

# Add To Cart Function

def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    product = get_object_or_404(Product, id=product_id)
    customer = request.user.customer

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    order_item.quantity += 1
    order_item.save()

    return redirect('cart')

# Remove From Cart Function

def remove_from_cart(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(OrderItem, id=item_id)

        if item.order.customer == request.user.customer:
            item.delete()
    return redirect('cart')

@login_required(login_url='login')
def checkout_view(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        street = request.POST.get('street')
        phone_number = request.POST.get('phone_number')

        customer = request.user.customer  
        order = Order.objects.get(customer=customer, complete=False)

        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = address,
            city = city,
            state = state,
            street = street,
            phone_number = phone_number,
        )

        return redirect('payment')

    return render(request, 'store/checkout.html')

def updateItem_view(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(
        user = request.user,
        name = request.user.username,
        )
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,
        complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)

# Auth Functions

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("store")
        else:
            # Wrong Informations, Redirect to Registeration Page
            messages.error(request, "بياناتك غير صحيحة, الرجاء التسجيل أولاً.")
            return redirect("login")
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form':form})

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            email = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone_number')
            customer, created = Customer.objects.get_or_create(user=user)
            customer.name = user.username
            customer.email = email
            customer.phone_number = phone_number
            customer.save()
                
            messages.success(request, "تم إنشاء الحساب بنجاح, الرجاء تسجيل الدخول.")
            return redirect('login')
        else:
            messages.error(request, 'فشل في التسجيل, قد يكون الإسم غير صالح أ, كلمة المرور ضعيفة.')
            return redirect('register')
    else:
        form = CustomUserCreationForm()
    return render(request, 'store/register.html', {'form': form})


#  Payment Function
@login_required(login_url='login')
def payment_view(request):
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')
        amount = request.POST.get('amount')
        customer = request.user.customer
        order = Order.objects.filter(customer = customer, complete=False).last()

        if order and amount:
            # Creating a Payment record
            Payment.objects.create(
                customer=customer,
                order=order,
                transaction_id=transaction_id,
                amount=amount,
            )
            # Marking the order as complete
            order.complete = True
            order.save()
            return redirect('waiting_confirmation')
               
    return render(request, 'store/payment.html')

def waiting_confirmation(request):
    customer = request.user.customer
    payment = Payment.objects.filter(customer=customer).order_by('-date_paid').first()
    return render(request, 'store/waiting_confirmation.html', {'payment': payment})
