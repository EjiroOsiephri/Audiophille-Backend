import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from paystackapi.transaction import Transaction as PaystackTransaction
from django.conf import settings
from django.http import HttpResponse

stripe.api_key = settings.STRIPE_SECRET_KEY




from django.http import HttpRequest

def index(request: HttpRequest):
    return HttpResponse("Welcome to the Ecommerce Backend!")


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


class StripeCheckoutSessionAPIView(APIView):
    def post(self, request):
        try:
            data = request.data
            # Create a Stripe Checkout Session
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {"name": data["product_name"]},
                            "unit_amount": int(data["amount"]) * 100,  # Price in cents
                        },
                        "quantity": data["quantity"],
                    },
                ],
                mode="payment",
                success_url="http://localhost:3000/success",  # Replace with your frontend success page URL
                cancel_url="http://localhost:3000/cancel",    # Replace with your frontend cancel page URL
            )
            return Response({"url": session.url})  # Send the URL for redirection
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
