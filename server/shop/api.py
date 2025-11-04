from rest_framework import viewsets, permissions, routers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.urls import path, include
from django.conf import settings
from .models import Product, Order, Payment
from .serializers import ProductSerializer, OrderSerializer, PaymentSerializer
from .payments import MockGateway, StripeGateway
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(active=True); serializer_class = ProductSerializer; permission_classes=[permissions.AllowAny]
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer; permission_classes=[permissions.IsAuthenticated]
    def get_queryset(self): return Order.objects.filter(user=self.request.user).prefetch_related("items__product")
    def perform_create(self, serializer): serializer.save(user=self.request.user)
    @action(detail=True, methods=["post"])
    def pay(self, request, pk=None):
        order = self.get_object(); token=request.data.get("token")
        provider = "stripe" if (getattr(settings,"STRIPE_API_KEY",None) and token) else "mock"
        gateway = StripeGateway(settings.STRIPE_API_KEY) if provider=="stripe" else MockGateway()
        result = gateway.charge(order.total_cents, token)
        pay = Payment.objects.create(order=order, provider=provider, provider_ref=result.ref, amount_cents=order.total_cents, status="succeeded" if result.ok else "failed")
        if result.ok: order.status="paid"; order.save(); return Response(PaymentSerializer(pay).data)
        return Response({"detail":"payment_failed"}, status=status.HTTP_402_PAYMENT_REQUIRED)
class ReportsViewSet(viewsets.ViewSet):
    permission_classes=[permissions.IsAuthenticated]
    def list(self, request):
        qs = Payment.objects.filter(order__user=request.user, status="succeeded")
        total = sum(p.amount_cents for p in qs); count = qs.count()
        return Response({"payments": count, "revenue_cents": total})
router=routers.DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"reports", ReportsViewSet, basename="reports")
urlpatterns=[path("", include(router.urls))]
