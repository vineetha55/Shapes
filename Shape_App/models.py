from django.db import models

# Create your models here.
class tbl_Category(models.Model):
    name = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True, choices=[('active', 'Active'), ('inactive', 'Inactive')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class tbl_SubCategory(models.Model):
    category = models.ForeignKey(tbl_Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100, null=True, choices=[('active', 'Active'), ('inactive', 'Inactive')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class tbl_Product(models.Model):
    subcategory = models.ForeignKey(tbl_SubCategory, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    material = models.CharField(max_length=100, null=True, blank=True)   # Cotton, Silk, etc.
    brand = models.CharField(max_length=100, null=True, blank=True)

    gender = models.CharField(max_length=10, choices=[
        ('men', 'Men'),
        ('women', 'Women'),
        ('kids', 'Kids'),
        ('unisex', 'Unisex'),
    ], default='unisex')

    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gst_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to="products/",null=True)

    def __str__(self):
        return self.name


# ✅ Separate table for product sizes (many-to-many)
class ProductSize(models.Model):
    product = models.ForeignKey(tbl_Product, on_delete=models.CASCADE, related_name="sizes")
    size = models.CharField(max_length=50, choices=[
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ])

    def __str__(self):
        return f"{self.product.name} - {self.size}"


# ✅ Separate table for product color variants with image
class ProductVariant(models.Model):
    product = models.ForeignKey(tbl_Product, on_delete=models.CASCADE, related_name="variants")
    color = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.product.name} - {self.color}"



class tbl_Signup(models.Model):
    fullname=models.CharField(max_length=100,null=True)
    email=models.EmailField(null=True)
    password=models.CharField(max_length=100,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class tbl_Cart(models.Model):
    user=models.ForeignKey(tbl_Signup, on_delete=models.CASCADE, related_name="user")
    product=models.ForeignKey(tbl_Product, on_delete=models.CASCADE, related_name="product_cart")
    quantity = models.IntegerField(null=True)
    selected_size=models.CharField(max_length=100,null=True)
    selected_color=models.CharField(max_length=100,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.quantity*self.product.price


class Address(models.Model):
    user = models.ForeignKey("tbl_Signup", on_delete=models.CASCADE, related_name="addresses")
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    pincode = models.CharField(max_length=10)
    house_name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    landmark = models.CharField(max_length=200, blank=True, null=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name}, {self.city}"


# Order model
class Order(models.Model):
    user = models.ForeignKey("tbl_Signup", on_delete=models.CASCADE, related_name="orders")
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    status_choices = [
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default="Pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} - {self.user.email}"


# OrderItem model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("tbl_Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # snapshot of product price

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_total(self):
        return self.quantity * self.price


class tbl_Wishlist(models.Model):
    user = models.ForeignKey(tbl_Signup, on_delete=models.CASCADE, related_name="wishlist")
    product = models.ForeignKey('tbl_Product', on_delete=models.CASCADE, related_name="wishlisted_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Prevent duplicates