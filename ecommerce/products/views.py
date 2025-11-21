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

   if category_id:
        products = products.filter(category__id=category_id)

    paginator = Paginator(products, 5)  # show 5 per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "products": page_obj.object_list,
        "categories": Category.objects.all(),
        "selected_category": category_id,
        "query": query,
    }

    return render(request, "products/product_list.html", context)
