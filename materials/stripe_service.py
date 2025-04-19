import os

import stripe

stripe.api_key = os.getenv("STRIPE_TEST_SECRET_KEY")


def create_product(name):
    product = stripe.Product.create(name=name)
    return product


def create_price(product_id, amount, currency="usd"):
    price = stripe.Price.create(
        unit_amount=amount,  # Указываем сумму в копейках
        currency=currency,
        product=product_id,
    )
    return price


def create_checkout_session(price_id):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="https://yourdomain.com/success",
        cancel_url="https://yourdomain.com/cancel",
    )
    return session
