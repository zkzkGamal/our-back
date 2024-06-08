from rest_framework import serializers
from .models import Drugs_Order, Order_Items

class OrderItemSerializer(serializers.ModelSerializer):
    total = serializers.FloatField(source='get_total', read_only=True)

    class Meta:
        model = Order_Items
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    total = serializers.FloatField(source='get_cart_total', read_only=True)
    total_quantity = serializers.IntegerField(source='get_cart_items', read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Drugs_Order
        fields = '__all__'






from rest_framework import serializers
from .models import Blog_Posts, Comment_Posts

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog_Posts
        fields = '__all__'

class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment_Posts
        fields = '__all__'
