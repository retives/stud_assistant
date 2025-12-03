from fastapi import APIRouter, HTTPException, status, Depends
from app.database import db_dependency
from app.schemas import SubscriptionCreate
from app.models import User
from app.routes.auth import get_current_user
from app.services.payment import init_customer, create_payment_intent
import stripe
from app.routes import get_user
router = APIRouter(prefix='/payments', tags=['payments'])

@router.get('/{payment_id}')
def payment_info():
    ...


@router.post("/subscribe")
def create_subscription(subscription: SubscriptionCreate, db = db_dependency, current_user = Depends(get_current_user)):
    user = get_user(db, current_user.id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    customer = init_customer(user)
    # Create subscription
    try:
        sub = stripe.Subscription.create(
            customer=customer.id,
            items=[{"price": subscription.price_id}],
            payment_behavior="default_incomplete",
            expand=["latest_invoice.payment_intent"]
        )
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))

    client_secret = sub.latest_invoice.payment_intent.client_secret
    return {"subscription_id": sub.id, "client_secret": client_secret}

@router.post('/')
def create_payment():
    ...