from django.urls import path

from . import views

app_name='payment'

urlpatterns = [
    path('', views.BasketView, name='basket'),
    path('add/', views.BasketView, name='basket_add'),
    path('orderplaced/', views.order_placed, name='order_placed'),
    path('webhook/', views.stripe_webhook),

]
