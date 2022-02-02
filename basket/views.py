from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from store.models import Product
from .basket import Basket
# Create your views here.
def basket_summary(request):
    basket = Basket(request)
    return render(request,'basket/summary.html',{'basket':basket})

def basket_add(request):
    
    basket = Basket(request)
    
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product,id=product_id)
        basket.add(product=product, product_qty=product_qty)

        return JsonResponse({'qty': basket.__len__()})

def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id  = int(request.POST.get('productid'))
        basket.delete(product_id=product_id)
        baskettotal = basket.get_total_price()
        return JsonResponse({'status': "deleted successfully","subtotal":baskettotal})

def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product_id=product_id,qty=product_qty)
        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({"qty":basketqty,'subtotal':baskettotal})
        return response