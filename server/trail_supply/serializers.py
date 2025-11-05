from rest_framework import serializers
from .models import Product, Order, OrderItem, Payment
class ProductSerializer(serializers.ModelSerializer):
    class Meta: model = Product; fields = ["id","name","price_cents","active","created_at"]
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source="product", write_only=True)
    class Meta: model = OrderItem; fields = ["id","product","product_id","quantity","line_total_cents"]
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta: model = Order; fields = ["id","created_at","total_cents","status","items"]
    def create(self, validated_data):
        items = validated_data.pop("items", []); order = Order.objects.create(**validated_data); total=0
        for it in items:
            product=it["product"]; qty=it.get("quantity",1); line=product.price_cents*qty
            OrderItem.objects.create(order=order, product=product, quantity=qty, line_total_cents=line); total+=line
        order.total_cents=total; order.save(); return order
class PaymentSerializer(serializers.ModelSerializer):
    class Meta: model = Payment; fields = ["id","order","provider","provider_ref","amount_cents","status","created_at"]
