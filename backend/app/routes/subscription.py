from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.responses import JSONResponse
from app.database import db_dependency
from app.schemas import CheckoutResponse, PlanSelection
from app.models import User
from app.routes.auth import get_current_user
from app.services.payment import init_customer
from app.limiter import limiter
import stripe
import os 

router = APIRouter(prefix='/payments', tags=['payments'])
WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')
PRICE_ID_MAP = {
    "plus_monthly": os.getenv('STRIPE_PRICE_ID_PLUS_MONTHLY'),

}
@limiter.limit("5/minute")
@router.post("/create-checkout-session", response_model=CheckoutResponse)
def create_checkout_session(request: Request, plan: PlanSelection, db: db_dependency, user: User = Depends(get_current_user)):
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

@limiter.limit("5/minute")
@router.post("/webhooks")
async def stripe_webhooks(request: Request, db: db_dependency):
    """
    Handles incoming Stripe Webhook events.
    Verifies the signature and processes critical subscription events.
    """
    
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    event = None

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

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        customer_id = session.get('customer')
        subscription_id = session.get('subscription')
        
        user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
        
        if user:
            user.is_plus_subscriber = True
            user.stripe_subscription_id = subscription_id 
            db.add(user)
            db.commit()
            print(f"Subscription actiзvated for user: {user.email}")
            
        else:
            print(f"Error: User not found for customer ID: {customer_id}")
        
    elif event['type'] == 'customer.subscription.deleted':
        session = event['data']['object']
        customer_id = session.get('customer')
        
        user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
        
        if user:
            user.is_plus_subscriber = False
            db.add(user)
            db.commit()
            print(f"Subscription deactivated for user: {user.email}")
            
    return JSONResponse(content={"success": True})