from dataclasses import dataclass
@dataclass
class PaymentResult: ok: bool; ref: str
class MockGateway:
    def charge(self, amount_cents: int, token: str | None = None) -> PaymentResult:
        return PaymentResult(ok=True, ref="MOCK-12345")
try:
    import stripe
except Exception:
    stripe = None
class StripeGateway:
    def __init__(self, api_key: str):
        if not stripe: raise RuntimeError("Stripe not installed")
        stripe.api_key = api_key
    def charge(self, amount_cents: int, token: str) -> PaymentResult:
        intent = stripe.PaymentIntent.create(amount=amount_cents, currency="usd", payment_method=token, confirm=True)
        return PaymentResult(ok=intent["status"]=="succeeded", ref=intent["id"])
