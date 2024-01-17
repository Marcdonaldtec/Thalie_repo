from django.urls import path
from .views import (product_list, search_products,product_views,
                    inventory_list, add_to_inventory,product_detail,
                    calculator, news_list, current_stock,
                    adjust_stock, stock_history,add_to_cart,
                    cart_view, update_cart,
                    remove_from_cart,checkout,thank_you,
                    register_user, login_user, 
                    logout_user, password_reset_request,
                    password_reset_confirm,user_profile,
                    edit_profile
)
urlpatterns = [
    # product section
    path('', product_views, name='product_views'),
    path('products', product_list, name='product_list'),
    path('products/search/', search_products, name='search_products'),
    path('products/<int:pk>/', product_detail, name='product_detail'), 
    path('calculator/', calculator, name='calculator'),
    path('inventory/', inventory_list, name='inventory_list'),
    path('inventory/add/<int:product_id>/', add_to_inventory, name='add_to_inventory'),
    path('news/', news_list, name='news_list'), 
    
    # manage stock
    path('current_stock/', current_stock, name='current_stock'),
    path('adjust_stock/<int:product_id>/', adjust_stock, name='adjust_stock'),
    path('stock_history/<int:product_id>/', stock_history, name='stock_history'),
    
    # Cart section 
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('update_cart/<int:cart_item_id>/<str:action>/', update_cart, name='update_cart'),
    path('remove_from_cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('thank_you/', thank_you, name='thank_you'),
    #  login_user
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('password_reset/', password_reset_request, name='password_reset_request'),
    path('password_reset_confirm/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
    # profile
    path('user_profile/', user_profile, name='user_profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
     
]
    # path('products/create/', create_product, name='create_product'),
    # path('products/<int:pk>/update/', update_product, name='update_product'),
    # path('products/<int:pk>/delete/', delete_product, name='delete_product'),




