from http.client import HTTPResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import stripe
import json

from orders.views import payment_confirmation
# Create your views here.
from basket.basket import Basket
import stripe

@login_required
def BasketView(request):
    basket = Basket(request)
    
    total = str(basket.get_total_price())

    total = total.replace('.','')
    total = int(total)
    
    stripe.api_key = 'sk_test_51KPCdrSFWJdREBSBcbkUw7rMwbIwbFVQieJuV2J5gDO9ncWGsmPXTfDTyz7tDUpu9n4ai2sfwV5vg5iHfLzPs4bG00f0mB5To2'
    
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency="inr",
        metadata={'userid':request.user.id}
    )
    return render(request, 'payment/home.html',{'client_secret':intent.client_secret})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body

    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        return HTTPResponse(status=400)

    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)
    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)

def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'payment/orderplaced.html')