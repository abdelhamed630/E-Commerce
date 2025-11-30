from django.shortcuts import get_object_or_404, render
from .models import Product, Category
from django.contrib.postgres.search import SearchVector
from cart.form import CartAddProductForm
from django.core.cache import cache
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request,category_slug=None ):

    data = Product.objects.filter( status = 'available')
    
    paginator = Paginator(data,6)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    categroy=None
    categroies=Category.objects.all()
    if category_slug:
              categroy=get_object_or_404(Category, slug=category_slug)
              page_obj = Product.objects.filter( category=categroy, status = 'available')   

    return render(request, 'index.html', { 'categories': categroies,
                    'category': categroy, 'page_obj': page_obj})


@login_required
def basse(request,category_slug=None ):
        categroy=None
        categroies=Category.objects.all()
        if category_slug:
              categroy=get_object_or_404(Category, slug=category_slug)
              data = Product.objects.filter( category=categroy, status = 'available')      
        quary=None
        results=[]
        if 'quary' in request.GET:
         quary=request.GET.get('quary')
         results=Product.objects.annotate(
           search=SearchVector('name', 'description'),
           ).filter(search=quary, status='available')
        context={'quary': quary, 'results': results,'categories': categroies, 'category': categroy}
        return render(request, 'base.html',context)


@login_required
def product_detail(request, product_slug):
    cache_key = f'product_{product_slug}'
    product = cache.get(cache_key)
    if  product is None:
         product = get_object_or_404(Product, slug=product_slug , status='available')
         cache.set(cache_key, product, timeout=60 * 30)  
    product = get_object_or_404(Product, slug=product_slug , status='available')
    cart_product_form = CartAddProductForm()
    return render(request, 'product_detail.html', {'product': product, 'cart_product_form': cart_product_form})

@login_required
def search(request):
    query=None
    results=[]
    if 'query' in request.GET:
        query=request.GET.get('query')
        results=Product.objects.annotate(
            search=SearchVector('name', 'description'),
        ).filter(search=query, status='available')
    context={'query': query, 'results': results}
    return render(request, 'search_results.html', context)



def about(request):
    return render(request, 'about.html')


def why_us(request):
    return render(request, 'why.html')

def testimonials(request):
    return render(request, 'testimonial.html')

