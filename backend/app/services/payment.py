import stripe
import os
from app.schemas import UserRead
"""
Note: Allow to save payment info
"""



# Add API key from env
stripe_key = os.getenv('STRIPE_KEY')
stripe.api_key = stripe_key

def init_customer(user):
    """Return existing Stripe customer if exists, otherwise create a new one."""
    if user.stripe_customer_id:
        # Customer already exists in Stripe
        return stripe.Customer.retrieve(user.stripe_customer_id)
    
    # Create new Stripe customer
    customer = stripe.Customer.create(email=user.email)
    
    # Here you should save the customer id in your DB
    user.stripe_customer_id = customer.id
    return customer


def create_payment_intent(customer_id: str, amount: int, currency: str = 'usd'):
    """Create a payment intent for a customer."""
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,
        customer=customer_id,
        payment_method_types=["card"],

    )
    return intent
