import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from paystackapi.transaction import Transaction as PaystackTransaction
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpRequest
import hashlib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from paystackapi.transaction import Transaction as PaystackTransaction
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def index(request: HttpRequest):
    return HttpResponse("Welcome to the Ecommerce Backend!")


class PaystackVerifyTransactionAPIView(APIView):
    def get(self, request, reference):
        try:
            # Verify the transaction using the reference
            response = PaystackTransaction.verify(reference)
            if response["data"]["status"] == "success":
                # Payment was successful
                return Response({"message": "Payment verified successfully", "data": response["data"]})
            else:
                # Payment not successful
                return Response({"message": "Payment not verified", "data": response["data"]}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StripePaymentAPIView(APIView):
    def post(self, request):
        try:
            data = request.data
            # Create a Stripe Payment Intent
            intent = stripe.PaymentIntent.create(
                amount=int(data['amount']),  # Amount in cents
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
            # Ensure `amount` represents the total price
            total_amount = int(data["amount"])  # Total amount in cents
            quantity = int(data["quantity"])  # Total quantity
            
            if quantity <= 0:
                return Response({'error': 'Quantity must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Calculate unit price
            unit_amount = total_amount // quantity  # Divide total amount by quantity
            
            # Create a Stripe Checkout Session
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {"name": data["product_name"]},
                            "unit_amount": unit_amount,  # Unit price in cents
                        },
                        "quantity": quantity,  # Correctly use quantity here
                    },
                ],
                mode="payment",
                success_url="https://audiophille-ecommerce.vercel.app/success",  # Replace with your frontend success page URL
                cancel_url="https://audiophille-ecommerce.vercel.app/checkout",    # Replace with your frontend cancel page URL
            )
            return Response({"url": session.url})  # Send the URL for redirection
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
                success_url="https://audiophille-ecommerce.vercel.app/success",  # Replace with your frontend success page URL
                cancel_url="https://audiophille-ecommerce.vercel.app/checkout",    # Replace with your frontend cancel page URL
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


@csrf_exempt
def paystack_webhook(request):
    if request.method == "POST":
        try:
            # Verify Paystack Signature
            paystack_secret_key = settings.PAYSTACK_SECRET_KEY
            signature = request.headers.get("x-paystack-signature", "")
            body = request.body

            if not hashlib.sha512(body + paystack_secret_key.encode()).hexdigest() == signature:
                return JsonResponse({"error": "Invalid signature"}, status=400)

            # Parse the event
            event = json.loads(request.body)
            if event["event"] == "charge.success":
                reference = event["data"]["reference"]
                # Confirm payment status
                response = PaystackTransaction.verify(reference)
                if response["data"]["status"] == "success":
                    # Handle successful payment
                    print("Payment Successful!")
                    return JsonResponse({"message": "Payment successful!"}, status=200)
            return JsonResponse({"message": "Unhandled event"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
