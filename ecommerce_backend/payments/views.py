import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from paystackapi.transaction import Transaction as PaystackTransaction
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripePaymentAPIView(APIView):
    def post(self, request):
        try:
            data = request.data
            # Create a Stripe Payment Intent
            intent = stripe.PaymentIntent.create(
                amount=int(data['amount']) * 100,  # Amount in cents
                currency='usd',
                payment_method_types=['card'],
                metadata={"email": data['email']}
            )
            return Response({'clientSecret': intent['client_secret']})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PaystackPaymentAPIView(APIView):
    def post(self, request):
        try:
            data = request.data
            # Initialize Paystack Transaction
            response = PaystackTransaction.initialize(
                reference=data['reference'],
                amount=int(data['amount']) * 100,  # Amount in kobo
                email=data['email']
            )
            return Response({'authorization_url': response['data']['authorization_url']})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
