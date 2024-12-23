from django.urls import path
from .views import StripePaymentAPIView, PaystackPaymentAPIView, StripeCheckoutSessionAPIView

urlpatterns = [
    path('stripe/', StripePaymentAPIView.as_view(), name='audiophille-stripe-payment'),
    path('stripe/checkout-session/', StripeCheckoutSessionAPIView.as_view(), name='audiophille-stripe-payment'),
    path('paystack/', PaystackPaymentAPIView.as_view(), name='audiophille-paystack-payment'),
    
]
