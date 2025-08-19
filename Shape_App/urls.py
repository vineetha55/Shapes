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
    path("shop_by_category/",views.shop_by_category,name="shop_by_category"),
    path("wishlist/",views.wishlist,name="wishlist"),
    path("signup/",views.signup,name="signup")

]