from decimal import Decimal

import pdfkit
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import *
# Create your views here.
def index(request):
    f_cat=tbl_Category.objects.filter(status="active")[:4]
    all_cat=tbl_Category.objects.filter(status="active")
    new_pdt=tbl_Product.objects.all().order_by('-id')[:4]
    top_pdt=tbl_Product.objects.all()[:8]
    context={
        "f_cat":f_cat,
        "new_pdt":new_pdt,
        "top_pdt":top_pdt,
        "all_cat":all_cat
    }
    return render(request,"index.html",context)

def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # --- Admin login (Django users) ---
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/Admin_Home/")

       
        if tbl_Signup.objects.filter(email=username, password=password).exists():
            customer = tbl_Signup.objects.get(email=username, password=password)
            request.session['userid'] = customer.id

            next_url = request.POST.get("next") or request.GET.get("next") or reverse("index")
            return redirect(next_url)

    return render(request, "signin.html", {
        "next": request.GET.get("next", "")
    })



def Admin_Home(request):
    return render(request,"Admin_Home.html")

def logout_view(request):
    logout(request)
    return redirect("index")


@login_required
def product_list(request):
    products = tbl_Product.objects.prefetch_related("sizes", "variants").all()
    return render(request, "product_list.html", {"products": products})


def add_product(request):
    subcategories = tbl_SubCategory.objects.all()

    if request.method == "POST":
        # Create Product
        product = tbl_Product.objects.create(
            subcategory_id=request.POST.get("subcategory"),
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            price=request.POST.get("price"),
            stock=request.POST.get("stock"),
            image=request.FILES.get("image"),
            material=request.POST.get("material"),
            brand=request.POST.get("brand"),
            gender=request.POST.get("gender"),
            status=request.POST.get("status"),
            gst_percentage=request.POST.get("gst_percentage")
        )

        # Add Sizes
        sizes = request.POST.getlist("size")
        for size in sizes:
            ProductSize.objects.create(product=product, size=size)

        # Add Colors
        colors = request.POST.getlist("color[]")
        for color in colors:
            if color.strip():
                ProductVariant.objects.create(product=product, color=color)

        return redirect("product_list")

    return render(request, "add_product.html", {"subcategories": subcategories})




from django.shortcuts import render, get_object_or_404, redirect
from .models import tbl_Product, tbl_SubCategory, ProductSize, ProductVariant

def edit_product(request, pk):
    product = get_object_or_404(tbl_Product, pk=pk)
    subcategories = tbl_SubCategory.objects.all()

    # Fetch existing sizes and colors
    existing_sizes = ProductSize.objects.filter(product=product).values_list("size", flat=True)
    existing_colors = ProductVariant.objects.filter(product=product).values_list("color", flat=True)

    if request.method == "POST":
        product.subcategory_id = request.POST.get("subcategory")
        product.name = request.POST.get("name")
        product.description = request.POST.get("description")
        product.price = request.POST.get("price")
        product.stock = request.POST.get("stock")
        if request.FILES.get("image"):
            product.image = request.FILES.get("image")
        product.material = request.POST.get("material")
        product.brand = request.POST.get("brand")
        product.gender = request.POST.get("gender")
        product.status = request.POST.get("status")
        product.gst_percentage = request.POST.get("gst_percentage")
        product.save()

        # Update Sizes
        ProductSize.objects.filter(product=product).delete()
        sizes = request.POST.getlist("size")
        for size in sizes:
            ProductSize.objects.create(product=product, size=size)

        # Update Colors
        ProductVariant.objects.filter(product=product).delete()
        colors = request.POST.getlist("color[]")
        for color in colors:
            if color.strip():
                ProductVariant.objects.create(product=product, color=color)

        return redirect("product_list")

    return render(
        request,
        "edit_product.html",
        {
            "product": product,
            "subcategories": subcategories,
            "existing_sizes": existing_sizes,
            "existing_colors": existing_colors,
        },
    )



def delete_product(request,id):
    product=tbl_Product.objects.get(id=id)
    product.delete()
    return redirect("product_list")
def stock_management(request):
    product=tbl_Product.objects.all()
    if request.method=="POST":
        s=tbl_Product.objects.get(id=request.POST.get("product"))
        print(s)
        s.stock+=int(request.POST.get("stock"))
        s.save()
        return redirect("product_list")
    return render(request,"stock_management.html",{"product":product})

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
    orders = Order.objects.select_related("user", "address").prefetch_related("items__product")
    return render(request, "all_sale.html", {"orders": orders})

@require_POST
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get("status")
    if new_status in dict(Order.status_choices):
        order.status = new_status
        order.save()
    return redirect("all_sale")

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.items.all()  # related_name="items" in OrderItem model
    return render(request, "order_detail.html", {"order": order, "order_items": order_items})


def print_label(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "print_label.html", {"order": order})

def print_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.items.all()
    return render(request, "print_invoice.html", {"order": order, "order_items": order_items})

def customers(request):
    customers = tbl_Signup.objects.all().order_by('-created_at')  # latest first
    return render(request, "customers.html", {"customers": customers})

def sales_report(request):
    # Default: show all orders
    orders = Order.objects.all().order_by("-created_at")

    # Filtering (optional: by date range)
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if start_date and end_date:
        orders = orders.filter(created_at__date__range=[start_date, end_date])

    # Calculate total sales
    total_sales = orders.aggregate(Sum("total_price"))["total_price__sum"] or 0

    return render(request, "sales_report.html", {
        "orders": orders,
        "total_sales": total_sales,
        "start_date": start_date,
        "end_date": end_date,
    })

def inventory_report(request):
    products = tbl_Product.objects.all().order_by('-created_at')

    # Get filter params
    date = request.GET.get("date")
    month = request.GET.get("month")
    year = request.GET.get("year")

    if date:
        products = products.filter(created_at__date=date)
    elif month and year:
        products = products.filter(created_at__month=month, created_at__year=year)
    elif year:
        products = products.filter(created_at__year=year)

    return render(request, "inventory_report.html", {
        "products": products,
        "selected_date": date,
        "selected_month": month,
        "selected_year": year,
    })
def cart(request):
    if request.session.get("userid"):
        cart_items=tbl_Cart.objects.filter(user=request.session['userid'])
        sub_total=sum(i.total_price() for i in cart_items)
        all_cat=tbl_Category.objects.filter(status="active")
        return render(request,"cart.html",{"all_cat":all_cat,"sub_total":sub_total,"cart_items":cart_items})
    return redirect("signin")

@csrf_exempt
def update_cart_quantity(request):
    if request.method == "POST":
        cart_id = request.POST.get("cart_id")
        quantity = int(request.POST.get("quantity"))

        try:
            cart_item = tbl_Cart.objects.get(id=cart_id)
            cart_item.quantity = quantity
            cart_item.save()

            # calculate subtotal for this user
            user = cart_item.user
            subtotal = tbl_Cart.objects.filter(user=user).aggregate(
                total=Sum(F('quantity') * F('product__price'))
            )['total'] or 0

            return JsonResponse({
                "success": True,
                "new_total": cart_item.total_price(),
                "subtotal": subtotal
            })
        except tbl_Cart.DoesNotExist:
            return JsonResponse({"success": False, "error": "Cart item not found"})


def products(request):
    product=tbl_Product.objects.filter(status="active")
    categories=tbl_Category.objects.filter(status="active")
    return render(request,"products.html",{"product":product,"all_cat":categories})


def shop_by_category(request,id):
    all_cat=tbl_Category.objects.filter(status="active")
    sub_cat = tbl_SubCategory.objects.filter(category=id)
    subcat_id = request.GET.get("subcategory")  # read query parameter
    if subcat_id:
        product = tbl_Product.objects.filter(subcategory_id=subcat_id)
    else:
        product = tbl_Product.objects.filter(subcategory__category__id=id)

    return render(request,"shop_by_category.html",{"sub_cat":sub_cat,"all_cat":all_cat,"product":product})

def wishlist(request):
    return render(request,"wishlist.html")


def signup(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Create user
        new_user = tbl_Signup.objects.create(
            fullname=fullname,
            email=email,
            password=password   # ⚠️ should hash in real apps
        )

        # Auto login
        request.session["userid"] = new_user.id

        # Redirect to next URL or index
        next_url = request.POST.get("next") or request.GET.get("next")
        if not next_url:
            next_url = reverse("index")
        return redirect(next_url)

    return render(request, "signup.html", {
        "next": request.GET.get("next", "")
    })


def add_to_cart(request, id):
    # Check if user is NOT logged in
    if not request.session.get("userid"):
        next_url = f"{reverse('add_to_cart', args=[id])}"
        return redirect(f"{reverse('signin')}?next={next_url}")

    color=request.POST.get("color")
    size=request.POST.get("size")
    if not color:
        color=ProductVariant.objects.filter(product=id).first()
    if not size:
        size = ProductSize.objects.filter(product=id).first()
    cart, created = tbl_Cart.objects.get_or_create(
        product_id=id,
        user_id=request.session["userid"],
        selected_color=color,
        selected_size=size,
        defaults={"quantity": 1}

    )
    if not created:
        cart.quantity += 1
        cart.save()

    return redirect("cart")

def remove_from_cart(request,id):
    data=tbl_Cart.objects.get(id=id)
    data.delete()
    return redirect("cart")

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import razorpay, json

razorpay_client = razorpay.Client(auth=("rzp_test_9zruMnoLDlsCLG", "oXUZ9Mf5zhjoZsTFLc7RpABO"))

def checkout(request):
    user = request.session['userid']
    addresses = Address.objects.filter(user=user)
    cart_items = tbl_Cart.objects.filter(user=user)
    amount = int(sum(item.product.price * item.quantity for item in cart_items) )* 100  # in paise
    razorpay_order = razorpay_client.order.create({"amount": amount, "currency": "INR", "payment_capture": "1"})
    return render(request, "checkout.html", {
        "addresses": addresses,
        "cart_items": cart_items,
        "amount": amount,
        "razorpay_key": "rzp_test_9zruMnoLDlsCLG",
        "razorpay_order_id": razorpay_order["id"],
    })
def add_address(request):
    if request.method=="POST":
        data=Address()
        data.full_name=request.POST.get("name")
        data.house_name = request.POST.get("house")
        data.city = request.POST.get("city")
        data.state = request.POST.get("state")
        data.pincode = request.POST.get("pincode")
        data.phone = request.POST.get("phone")
        data.landmark = request.POST.get("landmark")
        data.user_id=request.session['userid']
        data.save()
        return redirect("/checkout/")
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = json.loads(request.body)

        user_id = request.session.get("userid")
        if not user_id:
            return JsonResponse({"status": "error", "message": "User not logged in"}, status=400)

        address_id = data.get("address_id")
        if not address_id:
            return JsonResponse({"status": "error", "message": "Address not provided"}, status=400)

        cart_items = tbl_Cart.objects.filter(user=user_id)
        if not cart_items.exists():
            return JsonResponse({"status": "error", "message": "Cart is empty"}, status=400)

        # Calculate total
        print("jj")
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        # ✅ Save Razorpay details in order
        order = Order.objects.create(
            user_id=user_id,
            address_id=address_id,
            status="Paid",
            total_price=total_price,
            razorpay_order_id=data.get("razorpay_order_id"),
            razorpay_payment_id=data.get("razorpay_payment_id"),
            razorpay_signature=data.get("razorpay_signature"),
        )

        # Create OrderItems
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
                size=item.selected_size,
                color=item.selected_color
            )

        # Clear cart
        cart_items.delete()

        return JsonResponse({"status": "success", "order_id": order.id})



def order_success(request):
    user_id = request.session.get("userid")
    if not user_id:
        messages.error(request, "You must be logged in to view your orders.")
        return redirect("signin")

    # Get the latest order of this user
    order = Order.objects.filter(user_id=user_id).order_by("-id").first()

    if not order:
        messages.warning(request, "No recent orders found.")
        return redirect("cart")  # redirect to cart if no order

    # Get order items
    order_items = OrderItem.objects.filter(order=order)

    context = {
        "order": order,
        "order_items": order_items,
    }
    return render(request, "order_success.html", context)


def add_to_wishlist(request, id):
    if not request.session.get("userid"):
        messages.warning(request, "Please login to add items to your wishlist.")
        return redirect("signin")

    product = get_object_or_404(tbl_Product, id=id)

    wishlist_item, created = tbl_Wishlist.objects.get_or_create(user_id=request.session['userid'], product=product)

    if created:
        messages.success(request, f"{product.name} added to your wishlist!")
    else:
        messages.info(request, f"{product.name} is already in your wishlist.")

    return redirect("wishlist")  # Change redirect as per your site flow

def wishlist(request):
    if not request.session.get("userid"):
        return redirect("signin")

    wishlist_items = tbl_Wishlist.objects.filter(user=request.session['userid']).select_related("product")
    return render(request, "wishlist.html", {"wishlist_items": wishlist_items})

def remove_from_wishlist(request, id):
    if not request.session.get("userid"):
        messages.warning(request, "Please login to remove items from wishlist.")
        return redirect("signin")

    user_id = request.session["userid"]
    product = get_object_or_404(tbl_Product, id=id)

    wishlist_item = tbl_Wishlist.objects.filter(user_id=user_id, product=product).first()
    if wishlist_item:
        wishlist_item.delete()
        messages.success(request, f"{product.name} has been removed from your wishlist.")
    else:
        messages.warning(request, "This product is not in your wishlist.")

    return redirect("wishlist")

def product_single(request, id):
    product = get_object_or_404(tbl_Product, id=id, status="active")
    sizes = ProductSize.objects.filter(product=product).values_list("size", flat=True)
    colors = ProductVariant.objects.filter(product=product).values_list("color", flat=True)

    return render(request, "product_single.html", {
        "product": product,
        "sizes": list(sizes),
        "colors": list(colors),
    })


def my_account(request):
    user = request.session['userid']
    orders=Order.objects.filter(user=user)
    addresses = Address.objects.filter(user=user)
    profile=tbl_Signup.objects.filter(id=user)
    context={
        "orders":orders,
        "addresses":addresses,
        "profile":profile
    }
    return render(request,"my_account.html",context)

def signout(request):
    try:
        del request.session['userid']
        return redirect("/")
    except:
        return redirect("/")




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import tbl_Signup, Address, Order


# Edit Profile
def edit_profile(request,id):
    user_id = request.session.get("userid")
    profile = get_object_or_404(tbl_Signup, id=user_id)

    if request.method == "POST":
        profile.name = request.POST.get("name")
        profile.email = request.POST.get("email")
        profile.phone = request.POST.get("phone")
        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("my_account")

    return render(request, "edit_profile.html", {"profile": profile})


# Add Address
def add_address(request):
    user_id = request.session.get("userid")

    if request.method == "POST":
        Address.objects.create(
            user_id=user_id,
            full_name=request.POST.get("full_name"),
            phone=request.POST.get("phone"),
            address=request.POST.get("address"),
            city=request.POST.get("city"),
            state=request.POST.get("state"),
            zipcode=request.POST.get("zipcode"),
        )
        messages.success(request, "Address added successfully!")
        return redirect("my_account")

    return render(request, "add_address.html")


# Edit Address
def edit_address(request, id):
    address = get_object_or_404(Address, id=id)

    if request.method == "POST":
        address.full_name = request.POST.get("full_name")
        address.phone = request.POST.get("phone")
        address.address = request.POST.get("address")
        address.city = request.POST.get("city")
        address.state = request.POST.get("state")
        address.zipcode = request.POST.get("zipcode")
        address.save()
        messages.success(request, "Address updated successfully!")
        return redirect("my_account")

    return render(request, "edit_address.html", {"address": address})


# Order Detail
def order_detail(request, id):
    order = get_object_or_404(Order, id=id, user=request.session.get("userid"))
    return render(request, "order_detail.html", {"order": order})
