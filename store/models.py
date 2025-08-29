from django.db import models
from django.contrib.auth.models import User
from sequences import get_next_value

# customer model
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.name
    
# product model
class Product(models.Model):
    CATEGORY_CHOICES = (
        ('men', 'رجالي'),
        ('women', 'نسائي'),
        ('kids', 'أطفالي'),
    )
    CLOTHE_CATEGORY_CHOICES = (
        ('t-shirt', 'تي شيرتات'),
        ('shirts', 'قمصان'),
        ('pants', 'بناطلين'),
        ('jackets', 'جاكيتات'),
        ('suits', 'بدلات'),
        ('sportswear', 'ملابس رياضية'),
        ('jeans', 'جينز'),
        ('hoodies', 'هوديز'),
        ('dresses', 'فساتين'),
        ('blouses', 'بلوزات'),
        ('abayas', 'عبايات'),
        ('pajamas', 'بيجامات'),
        ('bags', 'حقائب'),
        ('sneakers', 'أحذية رياضية'),
        ('formal-shoes', 'أحذية رسمية'),
        ('boots', 'بوتات'),
        ('slippers', 'شباشب'),
        ('caps', 'كابات'),
        ('hats', 'قبعات'),
        ('sunglasses', 'نظارات شمسية'),
        ('watches', 'ساعات'),
)
    name = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=3, max_digits=10, default=0)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='men')
    type_of_clothe = models.CharField(max_length=20, choices=CLOTHE_CATEGORY_CHOICES, default='t-shirt')
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

# order model
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def save(self, *args, **kwargs):
        if not self.transaction_id:  
            next_val = get_next_value('order_transaction_id')
            self.transaction_id = str(next_val).zfill(4)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.transaction_id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

# order item model
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    def __str__(self):
        return str(self.product.name)

# shipping address model
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    street = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.address

# payment model
class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    date_paid = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False, verbose_name="Is Confirmed?")

    def __str__(self):
        return str(self.customer)