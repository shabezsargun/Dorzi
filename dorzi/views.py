import json
from pyexpat.errors import messages
from sqlite3 import IntegrityError
from contact.models import *
from porder.models import *
from product.models import *
from review.models import *
from tailor.models import *
from torder.models import *
from cart.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from functools import wraps
from django.contrib import messages  
from django.db.models import Q, Avg
import random
#-----------------------------------------------------------------------------------
#home

def tailor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to access this page.")
            return redirect('login')  
        if not hasattr(request.user, 'tailor'):  
            messages.error(request, "Access denied. This page is for tailors only.")
            return redirect('buyer_dashboard')  
        return view_func(request, *args, **kwargs)
    return wrapper

def user_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to access this page.")
            return redirect('login')
        if hasattr(request.user, 'tailor'):
            messages.error(request, "Access denied. This page is for buyers only.")
            return redirect('tailor_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if hasattr(user, 'tailor'):  
                    messages.error(request, "You are registered as a tailor. Please use the tailor login page.")
                    return redirect('tailor_login')  
                auth_login(request, user)
                messages.success(request, "Login successful!")  
                return redirect('home')  
            else:
                messages.error(request, "Invalid credentials. Please try again.")
        else:
            messages.error(request, "Form is not valid. Please check your input.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def tailor_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if not hasattr(user, 'tailor'):
                    messages.error(request, "You are not registered as a tailor. Please use the user login page.")
                    return redirect('user_login')
                auth_login(request, user)
                messages.success(request, "Tailor login successful!")
                return redirect('home')
            else:
                messages.error(request, "Invalid credentials. Please try again.")
        else:
            messages.error(request, "Form is not valid. Please check your input.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def login(request):
    return render(request, 'login.html')

def product_details(request, id):
    product = get_object_or_404(Product, id=id)
    random.shuffle(product)
    random_products = product[:10]
    reviews = Review.objects.filter(product=product)  
    return render(request, 'product_details.html', {'products': random_products, 'reviews': reviews})

def logout(request):
    auth_logout(request)  
    messages.success(request, "You have been logged out successfully.")  
    return redirect('home')  

def home(request):
    products = Product.objects.all() 
    review= Review.objects.all()
    return render(request, 'home.html', {'products': products, 'review': review})

def about(request):
    return render(request, 'about.html')

def terms(request):
    return render(request, 'terms.html')

def privacy(request):
    return render(request, 'privacy.html')

def findTailor(request):
    search_query = request.GET.get('search')  
    specialization = request.GET.get('specialization')  
    location = request.GET.get('location')  
    rating = request.GET.get('rating')  
    sort_criteria = request.GET.get('sort')  
    tailors = Tailor.objects.all()
    if search_query:
        tailors = tailors.filter(
            Q(business_name__icontains=search_query) | Q(services_offered__icontains=search_query)
        )
    if specialization:
        tailors = tailors.filter(expertise_details__icontains=specialization)
    if location:
        tailors = tailors.filter(business_location__icontains=location)
    if rating:
        if rating == "5":
            tailors = tailors.filter(average_rating__gte=5)
        elif rating == "4":
            tailors = tailors.filter(average_rating__gte=4)
        elif rating == "3":
            tailors = tailors.filter(average_rating__gte=3)
    if sort_criteria == "low-to-high":
        tailors = tailors.order_by('price')  
    elif sort_criteria == "high-to-low":
        tailors = tailors.order_by('-price')  
    elif sort_criteria == "rating":
        tailors = tailors.order_by('-average_rating')  
    return render(request, 'findTailor.html', {
        'tailors': tailors,
        'search_query': search_query,
        'specialization': specialization,
        'location': location,
        'rating': rating,
        'sort_criteria': sort_criteria,
    })
    
def readyMade(request):
    category = request.GET.get('category')
    rating = request.GET.get('rating')
    sort = request.GET.get('sort')
    search_query = request.GET.get('search')
    price_range = request.GET.get('price')
    products = Product.objects.all()
    if category:
        products = products.filter(tailor__expertise_details__icontains=category)
    if search_query:
        products = products.filter(name__icontains=search_query)
    if price_range:
        if price_range == 'under-500':
            products = products.filter(price__lt=500)
        elif price_range == '500-1000':
            products = products.filter(price__gte=500, price__lte=1000)
        elif price_range == 'over-1000':
            products = products.filter(price__gt=1000)
    if rating:
        products = products.annotate(avg_rating=Avg('product_reviews__rating')).filter(avg_rating__gte=int(rating))
    sort_mapping = {
        'low-to-high': 'price',
        'high-to-low': '-price',
        'rating': '-avg_rating',
    }
    if sort and sort in sort_mapping:
        if sort == 'rating':
            products = products.annotate(avg_rating=Avg('product_reviews__rating')).order_by(sort_mapping[sort])
        else:
            products = products.order_by(sort_mapping[sort])
    review = Review.objects.all()
    return render(request, 'readyMade.html', {
        'products': products,
        'review': review,
        'selected_category': category,
        'selected_rating': rating,
        'selected_sort': sort,
        'search_query': search_query,
        'selected_price': price_range,
    })
    
def tailor_details(request, id):
    tailor = get_object_or_404(Tailor, id=id)
    products = Product.objects.filter(tailor=tailor)
    reviews = Review.objects.filter(tailor=tailor)
    return render(request, 'tailor_details.html', {'tailor': tailor, 'products': products, 'reviews': reviews})

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('user_signup')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('user_signup')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return redirect('user_signup')
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            messages.success(request, "Signup successful!")
            return redirect('login')
        except IntegrityError:
            messages.error(request, "An error occurred while creating your account.")
            return redirect('user_signup')
    return render(request, 'signup.html')

def updateuser(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone = phone  
        try:
            user.save()
            messages.success(request, "User profile updated successfully.")
            return redirect("buyer_dashboard", id=user.id)  
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect("updateuser", id=user.id)
    return render(request, "update_profile.html", {"user": user})

def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.user != user:
        messages.error(request, "You cannot delete another user's account.")
        return redirect('dashboard')
    if request.method == 'POST':
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('home')  
    return render(request, 'delete_user.html', {'user': user})

def tailor_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        business_name = request.POST.get('business_name')
        business_location = request.POST.get('business_location')
        phone = request.POST.get('phone')
        expertise = request.POST.get('expertise')
        expertise_details = request.POST.get('expertise_details')
        price = request.POST.get('price')
        nid = request.POST.get('nid')
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')
        profile_picture = request.FILES.get('profile_picture')
        cover_images = request.FILES.getlist('cover_images')  
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('tailor_signup')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('tailor_signup')
        if Tailor.objects.filter(NID=nid).exists():
            messages.error(request, "NID already exists.")
            return redirect('tailor_signup')
        user = User.objects.create_user(username=username, email=email, password=password)
        tailor = Tailor.objects.create(
            user=user,
            business_name=business_name,
            business_location=business_location,
            phone=phone,
            expertise=expertise,
            expertise_details=expertise_details,
            price=price,
            NID=nid,
            category=category,  
            subcategory=subcategory,  
            profile_picture=profile_picture
        )
        for image in cover_images:
            TailorCoverImage.objects.create(tailor=tailor, image=image)
        auth_login(request, user)  
        messages.success(request, "Tailor account created successfully!")
        return redirect('login')  

    return render(request, 'tailor_signup.html')

def admin(request):
    product= Product.objects.all()
    tailor= Tailor.objects.all()
    review= Review.objects.all()
    torder= TOrders.objects.all()
    porder= Order.objects.all()
    contact= Contact.objects.all()
    cart= Cart.objects.all()
    return render(request, 'admin.html', {'product': product,'tailor':tailor,'review':review,'torder':torder,'porder':porder,'contact':contact,'cart':cart})

@tailor_required
def tailor_dashboard(request,id):
    tailor = get_object_or_404(Tailor, id=id)  
    product= Product.objects.all()
    review= Review.objects.all()
    torder= TOrders.objects.all()
    porder= Order.objects.all()
    return render(request, 'tailor_dashboard.html', {'tailor':tailor, 'product': product,'review':review,'torder':torder,'porder':porder})

@user_required
def buyer_dashboard(request,id):
    user = get_object_or_404(User, id=id) 
    porder= Order.objects.all()
    torder= TOrders.objects.all()
    review= Review.objects.all()
    return render(request, 'buyer_dashboard.html', {'porder': porder,'torder':torder,'review':review,'user':user})
#-----------------------------------------------------------------------------------
#contact

def createcontact(request):   
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        contact_message = Contact(name=name, email=email, message=message)
        contact_message.save()
        redirect_url = request.META.get('HTTP_REFERER', '/')
        return redirect(redirect_url) 
    return render(request, 'createcontact.html')

#-----------------------------------------------------------------------------------
#porder

def createporder(request, bid):
    buyer = get_object_or_404(get_user_model(), id=bid)
    if request.method == "POST":
        cart_items = CartItem.objects.filter(cart__user=buyer)
        if not cart_items.exists():
            return redirect("cart_page")  
        for item in cart_items:
            product = item.product
            tailor = product.tailor  
            Order.objects.create(
                buyer=buyer,
                tailor=tailor,
                product=product,
                quantity=item.quantity,
                price=product.price,
                address=buyer.address,
                number=buyer.phone_number,
                delivery_date=None        
            )
        cart_items.delete()
        return redirect("order_success") 
    return redirect("cart_page")

def deleteporder(request, id):
    order = get_object_or_404(Order, id=id)
    redirect_url = request.META.get('HTTP_REFERER', '/')  # Default to root if no referer
    order.delete()
    return redirect(redirect_url)
 #-----------------------------------------------------------------------------------
#torder 

def createtorder(request, bid, tid):
    if request.method == "POST":
        redirect_url = request.META.get('HTTP_REFERER', '/')
        buyer = get_object_or_404(User, id=bid)
        tailor = get_object_or_404(Tailor, id=tid)
        size = request.POST.get("size")
        fabrics = request.POST.get("fabrics")
        description = request.POST.get("description")
        measurement = request.POST.get("measurement")  
        address = request.POST.get("address")
        contact_number = request.POST.get("contact_number")
        delivery_date = request.POST.get("delivery_date")
        if not all([size, fabrics, description, address]):
            return render(request, "torder_form.html", {"error": "All fields except contact_number and delivery_date are required."})
        try:
            measurement = json.loads(measurement) if measurement else {}
        except json.JSONDecodeError as e:
            return render(request, "torder_form.html", {"error": f"Invalid measurement data: {str(e)}"})
        torder = TOrders.objects.create(
            buyer=buyer,
            tailor=tailor,
            size=size,
            fabrics=fabrics,
            description=description,
            measurement=measurement,
            address=address,
            contact_number=contact_number,
            delivery_date=delivery_date if delivery_date else None,
        )
        return redirect(redirect_url) 
    return render(request, "torder_form.html")  

def deletetorder(request, id):
    order = get_object_or_404(TOrders, id=id)
    redirect_url = request.META.get('HTTP_REFERER', '/')  
    order.delete()
    return redirect(redirect_url)

#-----------------------------------------------------------------------------------
#review

def createreviews(request, bid, tid, pid):
    referer_url = request.META.get('HTTP_REFERER', '/')
    if request.method == "POST":  
        user = get_object_or_404(get_user_model(), id=bid)
        tailor = get_object_or_404(Tailor, id=tid)
        product = get_object_or_404(Product, id=pid)
        rating = request.POST.get("rating")
        comment = request.POST.get("comment", "")  
        if not rating:
            return render(request, "/", {"error": "Rating is required."})
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError
        except ValueError:
            return render(request, "/", {"error": "Rating must be an integer between 1 and 5."})
        if Review.objects.filter(user=user, product=product).exists():
            return render(request, "readyMade.html", {"error": "You have already reviewed this product."})
        try:
            review = Review.objects.create(
                user=user,
                tailor=tailor,
                product=product,
                rating=rating,
                comment=comment
            )
        except ValueError as e:
            return render(request, "/", {"error": str(e)})
        messages.success(request, "Review submitted successfully.")
        return redirect(referer_url)  
    return render(request, "/") 


def updatereviews(request,id):
    review = get_object_or_404(Review, id=id)
    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment", "")  
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError
        except (ValueError, TypeError):
            return render(request, "review/review_update_form.html", {
                "error": "Rating must be an integer between 1 and 5.",
                "review": review
            })
        review.rating = rating
        review.comment = comment
        review.save()
        redirect_url = request.META.get('HTTP_REFERER', '/')
        messages.success(request, "Review updated successfully.")
        return redirect(redirect_url)  
    return render(request, "review_update_form.html", {"review": review})

def deletereviews(request,id):
    review = get_object_or_404(Review, id=id)
    redirect_url = request.META.get('HTTP_REFERER', '/')  
    review.delete()
    return redirect(redirect_url)
#-----------------------------------------------------------------------------------
#product

def createproduct(request,tid):
    referer_url = request.META.get('HTTP_REFERER', '/')
    tailor = get_object_or_404(Tailor, id=tid)
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        availability = request.POST.get("availability")
        price = request.POST.get("price")
        category = request.POST.get("category")
        images = request.FILES.getlist("images")  
        if not all([name, description, availability, price]):
            return render(request, "product_form.html", {"error": "Name, description, availability, and price are required.","tid": tid})
        try:
            availability = int(availability)
            price = float(price)
        except ValueError:
            return render(request, "product_form.html", {
                "error": "Availability must be an integer and price must be a number.",
                "tid": tid
            })
        product = Product.objects.create(
            name=name,
            description=description,
            availability=availability,
            price=price,
            tailor=tailor,
            category=category
        )
        for image in images:
            ProductImage.objects.create(product=product, image=image)
        messages.success(request, "Product created successfully.")
        return redirect(referer_url) 
    return render(request, "product_form.html", {"tid": tid})

def updateproduct(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        availability = request.POST.get("availability")
        price = request.POST.get("price")
        category = request.POST.get("category")
        images = request.FILES.getlist("images")  
        if not all([name, description, availability, price]):
            return render(request, "product/product_form.html", {
                "error": "Name, description, availability, and price are required.",
                "product": product
            })
        try:
            availability = int(availability)
            price = float(price)
        except ValueError:
            return render(request, "product/product_form.html", {
                "error": "Availability must be an integer and price must be a number.",
                "product": product
            })
        product.name = name
        product.description = description
        product.availability = availability
        product.price = price
        product.category = category
        if not product.category:
            return render(request, "product/product_form.html", {
                "error": "Category cannot be empty.",
                "product": product
            })
        product.save()
        if images:
            for image in images:
                ProductImage.objects.create(product=product, image=image)
        messages.success(request, "Product updated successfully.")
        return redirect("/")  
    return render(request, "tailor_dashboard.html", {
        "product": product
    })

def deleteproduct(request,id):
    product= get_object_or_404(Product,id=id)
    redirect_url = request.META.get('HTTP_REFERER', '/')
    product.delete()
    return redirect(redirect_url)

#-------------------------------------------------------------------------------------
#tailor

def updatetailor(request, id):
    tailor = get_object_or_404(Tailor, id=id)
    if request.method == "POST":
        business_name = request.POST.get("business_name", "").strip()
        business_location = request.POST.get("business_location", "").strip()
        phone = request.POST.get("phone", "").strip()
        expertise = request.POST.get("expertise", "").strip()
        expertise_details = request.POST.get("expertise_details", "").strip()
        price = request.POST.get("price", "").strip()
        category = request.POST.get("category", "").strip()
        subcategory = request.POST.get("subcategory", "").strip()
        profile_picture = request.FILES.get("profile_picture")
        cover_images = request.FILES.getlist("cover_images")
        if not all([business_name, business_location, expertise, price, category]):
            messages.error(request, "Please fill in all required fields.")
            return redirect("updatetailor", id=tailor.id)
        try:
            price = float(price)
        except ValueError:
            messages.error(request, "Price must be a valid number.")
            return redirect("updatetailor", id=tailor.id)
        tailor.business_name = business_name
        tailor.business_location = business_location
        tailor.phone = phone
        tailor.expertise = expertise
        tailor.expertise_details = expertise_details
        tailor.price = price
        tailor.category = category
        tailor.subcategory = subcategory
        if profile_picture:
            tailor.profile_picture = profile_picture
        tailor.save()
        for img in cover_images:
            TailorCoverImage.objects.create(tailor=tailor, image=img)
        messages.success(request, "Tailor profile updated successfully.")
        return redirect("tailor_dashboard", id=tailor.id)
    return render(request, "tailor_signup.html", {"tailor": tailor})

def deletetailor(request,id):
    tailor= get_object_or_404(Tailor,id=id)
    redirect_url = request.META.get('HTTP_REFERER', '/')
    tailor.delete()
    return redirect(redirect_url)

#-------------------------------------------------------------------------------------
#cart

@login_required
def remove_from_cart(request, bid):
    buyer = get_object_or_404(get_user_model(), id=bid)
    referer_url = request.META.get('HTTP_REFERER', '/')
    if request.method == "POST":
        cart = Cart.objects.filter(user=buyer).first()
        if not cart:
            messages.error(request, "Cart not found!")
            return redirect(referer_url)
        cart_items = cart.items.all()
        if not cart_items:
            messages.error(request, "Your cart is already empty.")
            return redirect(referer_url)
        for item in cart_items:
            product = item.product
            tailor = product.tailor
            product.popularity=+1
            Order.objects.create(
                buyer=buyer,
                tailor=tailor,
                product=product,
                quantity=item.quantity,
                price=product.price,
                address=item.address or "",
                number=item.number or "",
                delivery_date=None,
                size=item.size  
            )
        cart_items.delete()
        messages.success(request, "Order placed successfully!")
        return redirect(referer_url)
    return redirect(referer_url)

@login_required
def cart(request,bid):
    user = get_object_or_404(User, id=bid)
    cart, created = Cart.objects.get_or_create(user=user)  
    cart_items = CartItem.objects.filter(cart=cart)  
    return render(request, 'cart.html', {'cart_items': cart_items, 'user': user})  

@login_required
def add_to_cart(request, pid, bid):
    user = User.objects.get(id=bid)
    product = Product.objects.get(id=pid)
    cart, created = Cart.objects.get_or_create(user=user)
    referer_url = request.META.get('HTTP_REFERER', '/')

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        address = request.POST.get('address')
        number = request.POST.get('number')
        size = request.POST.get('size')  
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'size': size}  
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.address = address
            cart_item.number = number
            cart_item.size = size  
        else:
            cart_item.quantity = quantity
            cart_item.address = address
            cart_item.number = number
            cart_item.size = size
        cart_item.save()
        return redirect(referer_url)

def remove_from_cart_single(request, pid, bid):
    product = get_object_or_404(Product, id=pid)
    user = get_object_or_404(User, id=bid)
    cart = get_object_or_404(Cart, user=user)
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass  
    return redirect('cart', bid=user.id)
