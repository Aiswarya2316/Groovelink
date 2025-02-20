from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages




# Customer Registration
def customer_register(request):
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer registered successfully!")
            return redirect("login")
    else:
        form = CustomerRegistrationForm()
    return render(request, "customer/register.html", {"form": form, "user_type": "Customer"})



# Seller Registration
def seller_register(request):
    if request.method == "POST":
        form = StafRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Seller registered successfully!")
            return redirect("login")
    else:
        form = StafRegistrationForm()
    return render(request, "staf/register.html", {"form": form, "user_type": "Seller"})



# Admin Registration
def admin_register(request):
    if request.method == "POST":
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Admin registered successfully!")
            return redirect("login")
    else:
        form = AdminRegistrationForm()
    return render(request, "admin/register.html", {"form": form, "user_type": "Admin"})



# --- User Login ---
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = None
            redirect_url = "login"  # Default in case of failure

            if Customer.objects.filter(email=email, password=password).exists():
                user = Customer.objects.get(email=email)
                request.session["user_type"] = "Customer"
                redirect_url = "customerhome"
            elif Staf.objects.filter(email=email, password=password).exists():
                user = Staf.objects.get(email=email)
                request.session["user_type"] = "Seller"
                redirect_url = "stafhome"
            elif AdminReg.objects.filter(email=email, password=password).exists():
                user = AdminReg.objects.get(email=email)
                request.session["user_type"] = "Admin"
                redirect_url = "adminhome"

            if user:
                request.session["user_id"] = user.id
                messages.success(request, f"Welcome {user.name}!")
                return redirect(redirect_url)
            else:
                messages.error(request, "Invalid credentials")

    form = LoginForm()
    return render(request, "login.html", {"form": form})



# Logout View
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("home")




def home(request):
    return render(request,'home.html')


def stafhome(request):
    return render(request,'staf/stafhome.html')


def customerhome(request):
    return render(request,'customer/customerhome.html')


def adminhome(request):
    return render(request,'admin/adminhome.html')







from django.shortcuts import render, redirect
from django.contrib import messages
from .models import BandTeam, Product, Staf, Customer, AdminReg
from .forms import BandTeamForm, ProductForm, LoginForm

# --- Band Team Management ---
from django.contrib import messages

def add_band_team(request):
    if "user_id" not in request.session or request.session["user_type"] != "Seller":
        return redirect("login")

    staf = get_object_or_404(Staf, id=request.session["user_id"])

    if request.method == "POST":
        form = BandTeamForm(request.POST, request.FILES)
        if form.is_valid():
            band = form.save(commit=False)
            band.staf = staf
            band.save()
            messages.success(request, "Band team added successfully!")
            return redirect("view_band_teams")
        else:
            messages.error(request, "Failed to add band team. Please check the form.")
    
    form = BandTeamForm()
    return render(request, "staf/add_band_team.html", {"form": form})


def view_band_teams(request):
    if "user_id" not in request.session:
        return redirect("login")

    if request.session["user_type"] == "Admin":
        bands = BandTeam.objects.all()  # Admin sees all bands
    elif request.session["user_type"] == "Seller":
        staf = get_object_or_404(Staf, id=request.session["user_id"])
        bands = BandTeam.objects.filter(staf=staf)  # Seller sees only their bands
    else:
        return redirect("unauthorized")

    return render(request, "staf/view_band_teams.html", {"bands": bands})


# --- Product Management ---
def add_product(request):
    if "user_id" not in request.session or request.session["user_type"] != "Seller":
        return redirect("login")

    staf = Staf.objects.get(id=request.session["user_id"])

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.staf = staf
            product.save()
            return redirect("view_products")
    else:
        form = ProductForm()

    return render(request, "staf/add_product.html", {"form": form})

def view_products(request):
    if "user_id" not in request.session or request.session["user_type"] != "Seller":
        return redirect("login")

    staf = Staf.objects.get(id=request.session["user_id"])
    products = Product.objects.filter(staf=staf)
    return render(request, "staf/view_products.html", {"products": products})