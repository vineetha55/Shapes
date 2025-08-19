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
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gst_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)