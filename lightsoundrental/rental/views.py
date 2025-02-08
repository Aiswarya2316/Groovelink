from django.shortcuts import render

# Create your views here.
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import CustomUser, Product, Booking, Review
from .forms import UserSignUpForm, ShopOwnerSignUpForm, ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from decimal import Decimal
from django.contrib import messages



class UserSignUpView(CreateView):
    model = CustomUser
    form_class = UserSignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('product_list')

class ShopOwnerSignUpView(CreateView):
    model = CustomUser
    form_class = ShopOwnerSignUpForm
    template_name = 'registration/shop_owner_signup.html'
    success_url = reverse_lazy('shop_owner_login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_shop_owner = True
        user.save()
        return redirect('shop_owner_login')



class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        if self.request.user.is_shop_owner:
            return reverse_lazy('shop_owner_dashboard')
        return reverse_lazy('product_list')

class ShopOwnerLoginView(LoginView):
    template_name = 'registration/shop_owner_login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('shop_owner_dashboard')



# class ProductListView(ListView):
#     model = Product
#     template_name = 'products/product_list.html'
#     context_object_name = 'products'

#     def get_queryset(self):
#         return Product.objects.filter(is_available=True)

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Start by filtering for available products
        queryset = Product.objects.filter(is_available=True)

        # Check if pincode is provided in the GET parameters
        pincode_filter = self.request.GET.get('pincode')

        # If pincode is provided, filter by pincode
        if pincode_filter:
            queryset = queryset.filter(pincode=pincode_filter)

        return queryset

class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_create.html'
    success_url = reverse_lazy('shop_owner_dashboard')

    def test_func(self):
        return self.request.user.is_shop_owner

    def form_valid(self, form):
        form.instance.shop_owner = self.request.user
        # Set available_quantity equal to total_quantity initially
        form.instance.available_quantity = form.cleaned_data['total_quantity']
        return super().form_valid(form)

@login_required
def book_product(request, pk):
    if request.method == 'POST':
        product = Product.objects.get(pk=pk)
        # Add your dummy payment logic here
        booking = Booking.objects.create(
            user=request.user,
            product=product,
            start_date=request.POST['start_date'],
            end_date=request.POST['end_date'],
            total_price=request.POST['total_price'],
            payment_status=True  # Assuming payment is successful
        )
        return redirect('booking_confirmation', booking_id=booking.id)
    return redirect('product_list')


from django.db.models import Q 
from django.db import transaction



def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Check current bookings to determine availability for dates
    existing_bookings = Booking.objects.filter(
        product=product,
        end_date__gte=timezone.now().date(),
        returned = False
    )
    reviews = product.reviews.all()
    shop_owner = product.shop_owner  # Assuming product has a shop_owner field

    if request.method == 'POST' and request.user.is_authenticated:
        start_date = datetime.strptime(request.POST['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.POST['end_date'], '%Y-%m-%d').date()
        
        # Validate dates
        if start_date < timezone.now().date():
            messages.error(request, 'Start date cannot be in the past.')
            return render(request, 'products/product_detail.html', {'product': product})
        
        if end_date < start_date:
            messages.error(request, 'End date must be after start date.')
            return render(request, 'products/product_detail.html', {'product': product})
        
        # Check inventory availability for the requested dates
        conflicting_bookings = existing_bookings.filter(
            Q(start_date__lte=end_date) & Q(end_date__gte=start_date)
        ).count()
        
        if conflicting_bookings >= product.available_quantity:
            messages.error(request, 'Product not available for selected dates.')
            return render(request, 'products/product_detail.html', {'product': product})
        
        # Calculate price
        days = (end_date - start_date).days + 1
        total_price = product.price_per_day * Decimal(days)
        
        # Process payment
        payment_successful = process_dummy_payment(request.POST.get('card_number'))
        payment_successful= True
        if payment_successful:
            # Create booking and update inventory
            with transaction.atomic():
                booking = Booking.objects.create(
                    user=request.user,
                    product=product,
                    start_date=start_date,
                    end_date=end_date,
                    total_price=total_price,
                    payment_status=True
                )
                
                # Update available quantity
                product.available_quantity -= 1
                product.update_availability()
                
                messages.success(request, 'Booking successful!')
                return redirect('booking_confirmation', booking_id=booking.id)
        else:
            messages.error(request, 'Payment failed. Please try again.')
    
    # Calculate available dates
    booked_dates = []
    for booking in existing_bookings:
        current_date = booking.start_date
        while current_date <= booking.end_date:
            booked_dates.append(current_date)
            current_date += timedelta(days=1)
            
    context = {
        'product': product,
        'average_rating': product.average_rating(),
        'reviews': reviews,
        'booked_dates': booked_dates,
        'shop_owner': shop_owner,  # Pass the shop owner details to the template

    }
    
    return render(request, 'products/product_detail.html', context)

def process_dummy_payment(card_number):
    # Dummy payment processing - accepts if card number ends with '4242'
    return card_number and card_number.endswith('4242')

def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'bookings/booking_confirmation.html', {'booking': booking})


from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

class ShopOwnerDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_shop_owner

    def get(self, request):
        # Get all products of the shop owner
        products = Product.objects.filter(shop_owner=request.user)
        
        # Get all bookings for shop owner's products
        bookings = Booking.objects.filter(product__shop_owner=request.user)
        
        # Calculate recent bookings (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_bookings = bookings.filter(created_at__gte=thirty_days_ago)
        
        # Calculate statistics
        total_revenue = bookings.aggregate(Sum('total_price'))['total_price__sum'] or 0
        recent_revenue = recent_bookings.aggregate(Sum('total_price'))['total_price__sum'] or 0
        total_products = products.count()
        active_bookings = bookings.filter(returned = False).count()
        total_bookings = bookings.count()
        
        
        context = {
            'products': products,
            'recent_bookings': recent_bookings,
            'total_revenue': total_revenue,
            'recent_revenue': recent_revenue,
            'total_products': total_products,
            'active_bookings': active_bookings,
            'total_bookings': total_bookings,

        }
        
        return render(request, 'shop_owner_dashboard.html', context)
    

@login_required
def booking_return(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        with transaction.atomic():
            # Update product inventory
            product = booking.product
            product.available_quantity += 1
            product.update_availability()
            product.save()
            
            # Mark booking as returned
            booking.returned = True
            booking.return_date = timezone.now()
            booking.save()
            
            messages.success(request, 'Product returned successfully.')
            return redirect('shop_owner_dashboard')
    
    return render(request, 'bookings/booking_return.html', {'booking': booking})


@login_required
def user_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'bookings/user_bookings.html', {'bookings': bookings})


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def create_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Check if review already exists
    if hasattr(booking, 'review'):
        messages.error(request, 'You have already reviewed this booking.')
        return redirect('user_bookings')
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if rating and comment:
            Review.objects.create(
                booking=booking,
                user=request.user,
                product=booking.product,
                rating=rating,
                comment=comment
            )
            messages.success(request, 'Thank you for your review!')
            return redirect('product_detail', pk=booking.product.pk)
    
    return render(request, 'products/create_review.html', {'booking': booking})


def index(request):
    return render(request, 'premade/index.html')

def about(request):
    return render(request, 'premade/about-us.html')
def contact(request):
    return render(request, 'premade/contact-us.html')


from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .models import Product
from .forms import ProductForm

class ModifyProductView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/modify_product.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        # Get the product to modify
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        return product

    def form_valid(self, form):
        # Custom logic before saving the product
        response = super().form_valid(form)
        # Optionally, you can add some logic here after the product is saved.
        return response

    def get_success_url(self):
        # Redirect to product detail page after successful modification
        return reverse_lazy('product_detail', kwargs={'pk': self.object.pk})