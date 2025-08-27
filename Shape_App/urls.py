from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("signin/",views.signin,name="signin"),
    path("Admin_Home/",views.Admin_Home,name="Admin_Home"),
    path("logout/", views.logout_view, name="logout"),

    # Product Management
    path("product_list/", views.product_list, name="product_list"),
    path("products/add/", views.add_product, name="add_product"),
    path("products/stock/", views.stock_management, name="stock_management"),
    path("products/categories/", views.product_categories, name="product_categories"),
    path("products/sub_categories/",views.sub_categories,name="sub_categories"),
    path("category/add/",views.category_add,name="category_add"),
    path("subcategory/add/",views.subcategory_add,name="subcategory_add"),
    path('subcategories/edit/<int:id>/', views.subcategory_edit, name='subcategory_edit'),
    path('subcategories/delete/<int:id>/', views.subcategory_delete, name='subcategory_delete'),

    path("products/stock/update/<int:pk>/", views.update_stock, name="update_stock"),

    # Sales
    path("sales/all/", views.all_sale, name="all_sale"),
    path("customers/",views.customers,name="customers"),
    path("sales_report/",views.sales_report,name="sales_report"),
    path("inventory_report/",views.inventory_report,name="inventory_report"),
    path('categories/edit/<int:id>/', views.category_edit, name='category_edit'),
    path('categories/delete/<int:id>/', views.category_delete, name='category_delete'),
    path("cart/",views.cart,name="cart"),
    path("products/",views.products,name="products"),
    path("shop_by_category/<id>",views.shop_by_category,name="shop_by_category"),
    path("wishlist/",views.wishlist,name="wishlist"),
    path("signup/",views.signup,name="signup"),
    path("edit_product/<pk>",views.edit_product,name="edit_product"),
    path("delete_product/<id>",views.delete_product,name="delete_product"),
    path("add_to_cart/<id>",views.add_to_cart,name="add_to_cart"),
    path("update-cart/", views.update_cart_quantity, name="update_cart"),
    path("checkout/",views.checkout,name="checkout"),
    path("add_address/",views.add_address,name="add_address"),
    path("payment_success/",views.payment_success,name="payment_success"),
    path("order_success/",views.order_success,name="order_success"),
    path("print_invoice/<order_id>",views.print_invoice,name="print_invoice"),
    path("print_label/<order_id>",views.print_label,name="print_label"),
    path("update_order_status/<order_id>",views.update_order_status,name="update_order_status"),
    path("add_to_wishlist/<id>",views.add_to_wishlist,name="add_to_wishlist"),
    path("remove-from-wishlist/<int:id>/", views.remove_from_wishlist, name="remove_from_wishlist"),
    path("product_single/<id>",views.product_single,name="product_single"),
    path("remove_from_cart/<id>",views.remove_from_cart,name="remove_from_cart"),
    path("my_account/",views.my_account,name="my_account"),
    path("signout/",views.signout,name="signout"),
    path("edit-profile/<id>", views.edit_profile, name="edit_profile"),
    path("add-address/", views.add_address, name="add_address"),
    path("edit-address/<int:id>/", views.edit_address, name="edit_address"),
    path("order/<int:id>/", views.order_detail, name="order_detail"),


]