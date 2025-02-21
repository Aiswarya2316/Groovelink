from django.urls import path
from .import views
urlpatterns = [
    path('',views.home,name='home'),
    path("registerparent/", views.customer_register, name="customer_register"),
    path("registerstaf/", views.seller_register, name="seller_register"),
    path("registeradmin/", views.admin_register, name="admin_register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path('stafhome/',views.stafhome,name='stafhome'),
    path('customerhome/',views.customerhome,name='customerhome'),
    path('adminhome/',views.adminhome,name='adminhome'),
    path("addband/", views.add_band_team, name="add_band_team"),
    path("viewband/", views.view_band_teams, name="view_band_teams"),
    path("addproduct/", views.add_product, name="add_product"),
    path("viewproduct/", views.view_products, name="view_products"),
    path('about/',views.about,name='about'),
    path('viewbands/',views.viewbands,name='viewbands'),
    path('viewproducts/',views.viewproducts,name='viewproducts'),
    path('products/',views.products,name='products'),
    path('bands/',views.bands,name='bands'),
    path('users/',views.users,name='users'),
    path("book_band/<int:band_id>/", views.book_band, name="book_band"),
    path("booking_history/", views.booking_history, name="booking_history"),
    path("initiate_payment/<int:product_id>/<str:price>/", views.initiate_payment, name="initiate_payment"),
    path("payment_success/", views.payment_success, name="payment_success"),
    path("order_history/", views.view_order_history, name="order_history"),
    




]
