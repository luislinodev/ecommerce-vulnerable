from django.shortcuts import render, get_object_or_404
from .models import Catalog

def products(request):
    products = Catalog.objects.all()
    return render(request, 'catalog/catalog.html', {
        'products': products,
        'show_navbar': True,
    })

def product_detail(request, slug):
    product = get_object_or_404(Catalog, slug=slug)

    # Obtener productos sugeridos de la misma categoría, excluyendo el actual
    suggested_products = Catalog.objects.filter(
        categories=product.categories
    ).exclude(id=product.id)[:4]  # Limita a 4 sugerencias

    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'suggested_products': suggested_products,
        'show_navbar': True,
    })
