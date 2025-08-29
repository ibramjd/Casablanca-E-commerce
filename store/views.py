from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm

from .models import *

# store fucntion
def store_view(request):
    category = request.GET.get('category')
    type_of_clothe = request.GET.get('type_of_clothe')
    price = request.GET.get('price')

    products = Product.objects.all()

    if category:
        products = products.filter(category=category)
    if type_of_clothe:
        products = products.filter(type_of_clothe=type_of_clothe)
    if price:
        if price == 'low':
            products = products.filter(price__lt=10.000)
        elif price == 'mid':
            products = products.filter(price__gte=10.000, price__lt=25.000)
        elif price == 'high':
            products = products.filter(price__gte=25.000)

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
        'products': products,
        'items':items,
        'order':order,
        'category': category,
        'type_of_clothe': type_of_clothe,
        'price': price,
        }
    return render(request, 'store/store.html', context)

# shopping cart fucntion
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


# add to cart function
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

# remove from cart function
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(OrderItem, id=item_id)

        if item.order.customer == request.user.customer:
            item.delete()
    return redirect('cart')

# checkout fucntion
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

# login function
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("store")
        else:
            messages.error(request, "بياناتك غير صحيحة, الرجاء التسجيل أولاً.")
            return redirect("login")
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form':form})

# register fucntion
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


#  payment function
@login_required(login_url='login')
def payment_view(request):
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id')
        amount = request.POST.get('amount')
        customer = request.user.customer
        order = Order.objects.filter(customer = customer, complete=False).last()

        if order and amount:
            Payment.objects.create(
                customer=customer,
                order=order,
                transaction_id=transaction_id,
                amount=amount,
            )
            order.complete = True
            order.save()
            return redirect('waiting_confirmation')
               
    return render(request, 'store/payment.html')

# waiting payment confirmation fucntion
def waiting_confirmation(request):
    customer = request.user.customer
    payment = Payment.objects.filter(customer=customer).order_by('-date_paid').first()
    return render(request, 'store/waiting_confirmation.html', {'payment': payment})

# purchase history fucntion
@login_required(login_url='login')
def purchase_history_view(request):
    customer = request.user.customer
    payments = Payment.objects.filter(customer=request.user.customer).order_by('-date_paid')
    return render(request, 'store/purchase_history.html', {'payments': payments})