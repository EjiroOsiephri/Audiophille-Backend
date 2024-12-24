from django.urls import path
from .views import (
    StripePaymentAPIView,
    PaystackPaymentAPIView,
    StripeCheckoutSessionAPIView,
    index,
    paystack_webhook,
    PaystackVerifyTransactionAPIView,
    CryptoPaymentAPIView,
    crypto_webhook 
)

urlpatterns = [
    path('', index, name='audiophille-index'),
    path('stripe/', StripePaymentAPIView.as_view(), name='audiophille-stripe-payment'),
    path('stripe/checkout-session/', StripeCheckoutSessionAPIView.as_view(), name='audiophille-stripe-checkout-session'),
    path('paystack/', PaystackPaymentAPIView.as_view(), name='audiophille-paystack-payment'),
    path('paystack/webhook/', paystack_webhook, name='audiophille-paystack-webhook'),  
    path('api/payments/paystack/verify/<str:reference>/', PaystackVerifyTransactionAPIView.as_view(), name='paystack-verify'),
]
