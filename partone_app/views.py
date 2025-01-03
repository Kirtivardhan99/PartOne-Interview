from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from partone_app.models import *

def login_page(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            if email  in [None, "None", ""]:
                return "Please share proper email."
            
            user_obj = User.objects.filter(username = email)
            
            if not user_obj.exists():
                return "Account not Found", 400
                
            if not user_obj[0].profile.is_email_verified:
                return 'Your account is not verfiied', 400
            
            user_obj = authenticate(username = email, password = password)    
            
            if user_obj:
                return "User Logged in successfully", 200
            
    except Exception as e:  
        return str(e), 400


def register_page(request):
    try:
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username = email)
            
            if user_obj.exists():
                return "Email is already in use", 400
                
            user_obj = User.objects.create(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = email,
            )
            
            user_obj.set_password(password)
            user_obj.save()
            return "User Created Successfully", 200
    
    except Exception as e:  
        return str(e), 400
    

def add_product(request):
    try:
        if request.method == 'POST':
            product_name = request.POST.get('product_name')
            category_name = request.POST.get('category_name')
            product_description = request.POST.get('product_description')
            product_price = request.POST.get('product_price')
            product_quantity = request.POST.get('product_quantity')
            
            category = Category.objects.filter(name = category_name)
            
            if category.exists():
                product = Product.objects.filter(name = product_name, category__name = category[0].name)
            else:
                category = Category(
                    name = category_name,
                )
                category.save()
                
                product = Product.objects.filter(name = product_name, category__name = category[0].name)
            if product.exists():
                return "Product Already exists"
            
            else:
                product = Product(
                    name = product_name,
                    category = category,
                    product_description = product_description,
                )
                
                product.save()
                
                product_price = ProductPrice(
                    product = product,
                    price = product_price,
                )
                product_price.save()

                product_inventory = ProductInventory(
                    product = product,
                    stock_quantity = product_quantity,
                )
                
                product_inventory.save()
    except Exception as e:  
        return str(e), 400
    
    
def delete_product(request):
    try:
        if request.method == 'POST':
            product_name = request.POST.get('product_name')
            category_name = request.POST.get('category_name')
            
            category = Category.objects.filter(name = category_name)
            
            if category.exists():
                product = Product.objects.filter(name = product_name, category__name = category[0].name)
                if product.exists():
                    product[0].delete()
                    return "Product deleted successfully", 200
                else:
                    return "Product doesn't exist", 404
            else:
                return "Category doesn't exist", 404
    except Exception as e:  
        return str(e), 400
    
    
def get_product_details(request):
    try:
        if request.method == 'GET':
            product_name = request.get('product_name')
            category_name = request.POST.get('category_name')
            
            category = Category.objects.filter(name = category_name)
            
            if category.exists():
                product = Product.objects.filter(name = product_name, category__name = category[0].name)
                if product.exists():
                    return product[0].__dict__, 200
                else:
                    return "Product doesn't exist", 404
            else:
                return "Category doesn't exist", 404
    except Exception as e:  
        return str(e), 400
    
    
def update_product(request):
    try:
        if request.method == 'POST':
            product_name = request.POST.get('product_name')
            category_name = request.POST.get('category_name')
            product_description = request.POST.get('product_description')
            product_price = request.POST.get('product_price')
            product_quantity = request.POST.get('product_quantity')
            
            category = Category.objects.filter(name = category_name)
            
            if category.exists():
                product = Product.objects.filter(name = product_name, category__name = category[0].name)

                if product.exists():
                    if product_description not in [None, "None", ""]:
                        product[0].product_description = product_description
                        product.save()
                    
                    if product_price not in [None, "None", ""]:
                        product_price = ProductPrice.objects.filter(product = product[0])
                        product_price[0].price = product_price
                        product_price.save()
                        
                    if product_quantity not in [None, "None", ""]:
                        product_inventory = ProductInventory.objects.filter(product = product[0])
                        product_inventory[0].stock_quantity  = product_quantity
                        product_quantity.save()
                    
                    return "Success", 200
                
    except Exception as e:  
        return str(e), 400
