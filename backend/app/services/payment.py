import stripe
import os
from app.schemas import UserRead
from app.database import db_dependency
from app.models import User
"""
Note: Allow to save payment info
"""

stripe_key = os.getenv('STRIPE_KEY')
stripe.api_key = stripe_key

def init_customer(user: User, db: db_dependency):
    """Return existing Stripe customer if exists, otherwise create a new one."""
    
    # Check if the user already has a customer ID in your database
    if user.customer_id:
        try:
            return stripe.Customer.retrieve(user.customer_id)
        except stripe.error.InvalidRequestError:
            pass 
    
    # Create new Stripe customer
    customer = stripe.Customer.create(email=user.email)
    
    user.stripe_customer_id = customer.id
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return customer

