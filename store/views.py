from django.shortcuts import get_object_or_404, render

from .models import Category, Product

# Create your views here.


def all_products(request):
    product_list = Product.objects.prefetch_related("product_image").filter(
        is_active=True
    )[:20]
    return render(request, "store/index.html", {"product_list": product_list})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    user = request.user
    if user.is_authenticated:
        wishlist = Product.objects.filter(users_wishlist=request.user)
    else:
        wishlist = []
    return render(
        request, "store/single.html", {"product": product,
                                       "wishlist": wishlist}
    )


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(
        category__in=Category.objects.get(slug=category_slug).get_descendants(
            include_self=True
        )
    )
    return render(
        request,
        "store/category.html",
        {"category": category, "products": products},
    )
