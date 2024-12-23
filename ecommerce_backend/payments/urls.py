from django.urls import path
from .views import StripePaymentAPIView, PaystackPaymentAPIView

urlpatterns = [
    path('stripe/', StripePaymentAPIView.as_view(), name='stripe-payment'),
    path('paystack/', PaystackPaymentAPIView.as_view(), name='paystack-payment'),
]
