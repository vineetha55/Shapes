from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import *
# Create your views here.
def index(request):
    return render(request,"index.html")

def signin(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("/Admin_Home/")
    return render(request,"signin.html")

def Admin_Home(request):
    return render(request,"Admin_Home.html")

def logout_view(request):
    logout(request)
    return redirect("index")



@login_required
def product_list(request):
    products=tbl_Product.objects.all()
    context={
        "products":products,
    }
    return render(request, "product_list.html",context)

def add_product(request):
    return render(request,"add_product.html")


def stock_management(request):
    return render(request,"stock_management.html")

def product_categories(request):
    data=tbl_Category.objects.all()
    return render(request,"product_categories.html",{"data":data})


def category_edit(request,id):
    data=tbl_Category.objects.get(id=id)
    if request.method=="POST":
        obj=tbl_Category.objects.get(id=id)
        obj.name=request.POST.get("name")
        obj.status=request.POST.get("status")
        obj.save()
        return redirect("product_categories")
    return render(request,"category_edit.html",{"data":data})

def category_delete(request,id):
    data=tbl_Category.objects.get(id=id)
    data.delete()
    return redirect("product_categories")

def sub_categories(request):
    data=tbl_SubCategory.objects.all()
    return render(request,"sub_categories.html",{"data":data})

def category_add(request):
    if request.method == "POST":
        obj = tbl_Category()
        obj.name = request.POST.get("name")
        obj.status = request.POST.get("status")
        obj.save()
        return redirect("product_categories")
    return render(request,"category_add.html")

def subcategory_add(request):
    data=tbl_Category.objects.filter(status="active")
    if request.method == "POST":
        category_id = request.POST.get("category")
        name = request.POST.get("name")
        status = request.POST.get("status")
        tbl_SubCategory.objects.create(category_id=category_id,name=name,status=status)
        return redirect("sub_categories")
    return render(request,"subcategory_add.html",{"data":data})

# Subcategory Edit
def subcategory_edit(request, id):
    subcategory = get_object_or_404(tbl_SubCategory, id=id)
    categories = tbl_Category.objects.filter(status="active")  # only active categories

    if request.method == "POST":
        category_id = request.POST.get("category")
        name = request.POST.get("name")
        status = request.POST.get("status")

        if category_id and name:
            category = get_object_or_404(tbl_Category, id=category_id)
            subcategory.category = category
            subcategory.name = name
            subcategory.status = status
            subcategory.save()
            messages.success(request, "✅ Subcategory updated successfully!")
            return redirect("sub_categories")
        else:
            messages.error(request, "⚠️ Please fill all required fields")

    return render(request, "subcategory_edit.html", {
        "subcategory": subcategory,
        "categories": categories
    })


# Subcategory Delete
def subcategory_delete(request, id):
    subcategory = get_object_or_404(tbl_SubCategory, id=id)
    subcategory.delete()
    messages.success(request, "🗑️ Subcategory deleted successfully!")
    return redirect("sub_categories")
def update_stock(request):
    return render(request,"update_stock.html")

def all_sale(request):
    return render(request,"all_sale.html")

def customers(request):
    return render(request,"customers.html")

def sales_report(request):
    return render(request,"sales_report.html")

def inventory_report(request):
    return render(request,"inventory_report.html")


def cart(request):
    return render(request,"cart.html")

def products(request):
    return render(request,"products.html")


def shop_by_category(request):
    return render(request,"shop_by_category.html")

def wishlist(request):
    return render(request,"wishlist.html")

def signup(request):
    return render(request,"signup.html")