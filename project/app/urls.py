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

]
