# urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView  # Import Django's built-in LogoutView

urlpatterns = [
    path('',views.index, name='index'),
    path('about/',views.about, name='about'),

    path('contact/',views.contact, name='contact'),

    path('product/list', views.ProductListView.as_view(), name='product_list'),
    path('signup/', views.UserSignUpView.as_view(), name='user_signup'),
    path('shop-owner/signup/', views.ShopOwnerSignUpView.as_view(), name='shop_owner_signup'),
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/book/', views.book_product, name='book_product'),
    path('product/<int:pk>/modify/', views.ModifyProductView.as_view(), name='modify_product'),

    path('login/', views.UserLoginView.as_view(), name='login'),
    path('shop-owner/login/', views.ShopOwnerLoginView.as_view(), name='shop_owner_login'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('booking/<int:booking_id>/confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('shop-owner/dashboard/', views.ShopOwnerDashboardView.as_view(), name='shop_owner_dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),  # Logout URL
    path('booking/<int:booking_id>/return/', views.booking_return, name='booking_return'),
    path('bookings/', views.user_bookings, name='user_bookings'),
    path('booking/<int:booking_id>/review/', views.create_review, name='create_review'),

]