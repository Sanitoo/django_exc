from django.shortcuts import render, redirect
from .models import Product, Category
from .forms import ProductForm, CategoryForm

def home(request):
    return render(request, "products/home.html")

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            # pass message
            return redirect("products:add_category")
    else:
        form = CategoryForm()
    return render(request,"products/category_form.html",{'form':form})

def category_list(request):
    categories = Category.objects.all()
    return render(request,"products/category_list.html",{'categories':categories})

def product_list(request):
    """
    Added:
    - Search by product name
    - Filter by category
    - Pagination
    """
    query = request.GET.get("q", "")
    category_id = request.GET.get("category", "")

    products = Product.objects.all()

 if query:
        products = products.filter(name__icontains=query)
