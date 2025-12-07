from fastapi import APIRouter, HTTPException, status, Depends, Request, JSONResponse
from app.database import db_dependency
from app.schemas import CheckoutResponse, PlanSelection
from app.models import User
from app.routes.auth import get_current_user
from app.services.payment import init_customer, create_payment_intent
import stripe

import os 

router = APIRouter(prefix='/payments', tags=['payments'])
WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')
PRICE_ID_MAP = {
    "plus_monthly": os.getenv('STRIPE_PRICE_ID_PLUS_MONTHLY'),

}

@router.post("/create-checkout-session", response_model=CheckoutResponse)
def create_checkout_session(plan: PlanSelection, db: db_dependency, user: User = Depends(get_current_user)):
    """
    1. Ensures the user has a Stripe Customer ID.
    2. Creates the Stripe Checkout Session for subscription.
    """
    
    stripe_price_id = PRICE_ID_MAP.get(plan.selected_plan)
    if not stripe_price_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid plan selected."
        )

    try:
        stripe_customer = init_customer(user, db)
    except Exception as e:
        print(f"Error initializing customer: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Could not prepare customer for checkout."
        )

    try:
        session = stripe.checkout.Session.create(
            customer=user.customer_id, 
            payment_method_types=['card'],
            mode="subscription",
            line_items=[{"price": stripe_price_id, "quantity": 1}],
            
            success_url=f"{os.getenv('FRONTEND_URL')}/payments/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{os.getenv('FRONTEND_URL')}/payments/cancel",
        )
    except Exception as e:
        print(f"Error creating Stripe Session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to create checkout session with Stripe."
        )
        
    return CheckoutResponse(url=session.url)

@router.post("/webhooks")
async def stripe_webhooks(request: Request, db: db_dependency):
    """
    Handles incoming Stripe Webhook events.
    Verifies the signature and processes critical subscription events.
    """
    
    # 1. Get the raw request body and signature
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    event = None

    # 2. Verify the webhook signature for security
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise HTTPException(status_code=400, detail="Invalid signature")

    # 3. Handle the event type
    # We are primarily interested in confirming a successful checkout session.
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Data we need:
        customer_id = session.get('customer')
        subscription_id = session.get('subscription')
        
        # Important: Retrieve the user from your database using the Stripe Customer ID
        user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
        
        if user:
            # 4. Activate the user's subscription status in your DB
            user.is_plus_subscriber = True
            user.stripe_subscription_id = subscription_id # Save the sub ID for cancellation/management
            db.add(user)
            db.commit()
            print(f"Subscription activated for user: {user.email}")
            
        else:
            # Log an error if a customer ID from Stripe doesn't match a user in your DB
            print(f"Error: User not found for customer ID: {customer_id}")
            # You might want to contact the user or log this for manual review
        
    elif event['type'] == 'customer.subscription.deleted':
        # Handle subscription cancellation or expiration
        session = event['data']['object']
        customer_id = session.get('customer')
        
        user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
        
        if user:
            user.is_plus_subscriber = False
            db.add(user)
            db.commit()
            print(f"Subscription deactivated for user: {user.email}")
            
    # Add handlers for other events as your app grows (e.g., invoice.payment_failed)

    # 5. Return a 200 OK status to Stripe
    return JSONResponse(content={"success": True})