from rest_framework import serializers
from .models import Category,Product,Review

class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

        #exclude = ''.split() исключение

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
          model = Product
          fields = '__all__'

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProductReviewSerializer(serializers.ModelSerializer):
    review = ReviewSerializer(many=True, read_only=True)
    rating = serializers.FloatField(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'





