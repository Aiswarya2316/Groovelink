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
from django.shortcuts import render, redirect
from .models import BandTeam, Booking
from django.utils.timezone import now




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


from django.shortcuts import render
from .models import Customer, Product, BandTeam, Order

def adminhome(request):
    total_users = Customer.objects.count()
    total_products = Product.objects.count()
    total_bands = BandTeam.objects.count()
    total_orders = Order.objects.count()
    total_bookings=Booking.objects.count()

    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_bands': total_bands,
        'total_orders': total_orders,
        'total_bookings':total_bookings
    }
    return render(request, 'admin/adminhome.html', context)








from django.shortcuts import render, redirect
from django.contrib import messages
from .models import BandTeam, Product, Staf, Customer, AdminReg
from .forms import BandTeamForm, ProductForm, LoginForm

# --- Band Team Management ---
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import BandTeam, Staf
from .forms import BandTeamForm

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


def about(request):
    return render(request,'customer/about.html')

def viewbands(request):
    band=BandTeam.objects.all()
    return render(request,'customer/viewbands.html',{'band':band})


def viewproducts(request):
    products = Product.objects.all()
    days_range = range(1, 31)  # Generate the range in Python
    return render(request, 'customer/viewproducts.html', {'products': products, 'days_range': days_range})












import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order
from django.http import JsonResponse

# Initialize Razorpay Client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def initiate_payment(request, product_id, days, total_price):
    product = get_object_or_404(Product, id=product_id)
    
    # Create a Razorpay Order
    order_data = {
        "amount": float(total_price) * 100,  # Convert to paisa
        "currency": "INR",
        "payment_capture": "1"
    }
    
    razorpay_order = razorpay_client.order.create(order_data)
    
    context = {
        "product": product,
        "order_id": razorpay_order["id"],
        "amount": order_data["amount"],
        "days": days,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
    }
    return render(request, "customer/payment.html", context)


from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Product, Order, Customer  # Ensure Customer model is imported

def payment_success(request):
    if request.method == "POST":
        if "user_id" in request.session and request.session.get("user_type") == "Customer":
            customer_id = request.session["user_id"]
            try:
                customer = Customer.objects.get(id=customer_id)
            except Customer.DoesNotExist:
                messages.error(request, "Customer not found.")
                return redirect("login")

            order_id = request.POST.get("order_id")
            payment_id = request.POST.get("razorpay_payment_id")
            product_id = request.POST.get("product_id")

            product = get_object_or_404(Product, id=product_id)

            order = Order.objects.create(
                customer=customer,
                product=product,
                total_amount=product.price,
                payment_status=True,
                order_status="Processing",
            )

            return redirect("order_history")
        else:
            messages.error(request, "You need to log in to complete the payment.")
            return redirect("login")

    return JsonResponse({"error": "Invalid request"}, status=400)



def view_order_history(request):
    if "user_id" in request.session and request.session.get("user_type") == "Customer":
        customer_id = request.session["user_id"]
        print("Logged-in User ID:", customer_id)  # Debugging

        try:
            customer = Customer.objects.get(id=customer_id)  # Fetch the specific customer
            orders = Order.objects.filter(customer=customer).order_by("-created_at")  # Filter only their orders

            return render(request, "customer/order_history.html", {"orders": orders})
        except Customer.DoesNotExist:
            messages.error(request, "Customer not found.")
            return redirect("login")

    messages.error(request, "You need to log in to view your bookings.")
    return redirect("login")




import razorpay
import json
from django.conf import settings
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from .models import BandTeam, Booking, Customer
from datetime import datetime
from razorpay.errors import SignatureVerificationError

# ✅ Booking View with Razorpay Integration
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
def book_band(request, band_id):
    if request.method == "POST":
        band = BandTeam.objects.get(id=band_id)
        event_date = request.POST.get("event_date")
        customer_email = request.POST.get("email")

        event_date_obj = datetime.strptime(event_date, "%Y-%m-%d").date()
        if event_date_obj < now().date():
            messages.error(request, "Event date cannot be in the past.")
            return redirect("viewbands")

        # ✅ Fetch customer using email
        try:
            customer = Customer.objects.get(email=customer_email)
        except Customer.DoesNotExist:
            messages.error(request, "Customer not found. Please provide a valid email.")
            return redirect("viewbands")

        # ✅ Create Razorpay Order
        amount = int(band.booking_fee * 100)  # Convert to paise
        order_data = {
            "amount": amount,
            "currency": "INR",
            "payment_capture": "1",
        }
        order = client.order.create(order_data)

        # ✅ Store booking details in session
        request.session["booking_details"] = {
            "customer_email": customer_email,
            "band_id": band.id,
            "event_date": event_date,
            "order_id": order["id"],
            "amount": amount,
        }

        return render(request, "customer/payment_page.html", {
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "order_id": order["id"],
            "amount": band.booking_fee,  
            "band": band,
        })

    return redirect("viewbands")


from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import razorpay
from django.conf import settings
from .models import BandTeam, Booking, Customer
from razorpay.errors import SignatureVerificationError

from django.http import JsonResponse

@csrf_exempt
def paymentsuccess(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            razorpay_payment_id = data.get("razorpay_payment_id")
            razorpay_order_id = data.get("razorpay_order_id")
            razorpay_signature = data.get("razorpay_signature")

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            params_dict = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            }
            client.utility.verify_payment_signature(params_dict)

            booking_details = request.session.get("booking_details")
            if not booking_details:
                return JsonResponse({"success": False, "message": "Session expired. Please try again."}, status=400)

            customer = Customer.objects.get(email=booking_details["customer_email"])
            band = BandTeam.objects.get(id=booking_details["band_id"])

            booking, created = Booking.objects.get_or_create(
                customer=customer,
                band=band,
                event_date=booking_details["event_date"],
                defaults={"status": "Confirmed", "payment_id": razorpay_payment_id}
            )

            if not created:
                booking.status = "Confirmed"
                booking.payment_id = razorpay_payment_id
                booking.save()

            request.session.pop("booking_details", None)
            return JsonResponse({
                "status": "success",
                "redirect_url": reverse("booking_history")
            })



        except SignatureVerificationError:
            return JsonResponse({"success": False, "message": "Payment verification failed. Please contact support."}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Error: {e}"}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)


from django.contrib import messages
from .models import Booking, Customer  # Ensure Booking and Customer are imported

def booking_history(request):
    if "user_id" in request.session and request.session.get("user_type") == "Customer":
        customer_id = request.session["user_id"]

        try:
            customer = Customer.objects.get(id=customer_id)
            bookings = Booking.objects.filter(customer=customer, status="Confirmed").order_by("-created_at")
            return render(request, "customer/booking_history.html", {"bookings": bookings})

        except Customer.DoesNotExist:
            messages.error(request, "Customer not found.")
            return redirect("login")

    messages.error(request, "You need to log in to view your booking history.")
    return redirect("login")






def products(request):
    pro=Product.objects.all()
    return render(request,'admin/products.html',{'pro':pro})

def bands(request):
    bnd=BandTeam.objects.all()
    return render(request,'admin/bands.html',{'bnd':bnd})

def users(request):
    usr=Customer.objects.all()
    return render(request,'admin/users.html',{'usr':usr})

def orders(request):
    ordr=Order.objects.all()
    return render(request,'admin/orders.html',{'ordr':ordr})

def bookings(request):
    bkngs=Booking.objects.all()
    return render(request,'admin/bookings.html',{'bkngs':bkngs})


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Booking  # Replace with your actual model name

def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == "POST":
        booking.status = "Cancelled"
        booking.save()
        messages.success(request, "Booking cancelled successfully.")
    
    return redirect('booking_history')  # Adjust this to your actual bookings view name


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Order  # Replace with your actual model name

def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        order.order_status = "Cancelled"
        order.save()
        messages.success(request, "Order cancelled successfully.")
    
    return redirect('order_history')  # Replace with the actual name of your order history view


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Booking, Feedback  # assuming you have a Feedback model

def give_feedback(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        feedback_text = request.POST.get('feedback')
        Feedback.objects.create(
            booking=booking,
            customer=request.user,  # assuming the user is logged in
            comment=feedback_text
        )
        messages.success(request, 'Thank you for your feedback!')
        return redirect('booking_history')

    return render(request, 'customer/feedback_form.html', {'booking': booking})




def delete_band(request, id):
    band = get_object_or_404(BandTeam, id=id)
    band.delete()
    return redirect('view_band_teams')  # Replace with your actual view name

from django.shortcuts import redirect, get_object_or_404
from .models import Product  # adjust import as needed

def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('view_products')  # replace with the actual name of your view
