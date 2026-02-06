from rest_framework import serializers
from .models import Category, Product, Review, CHOICES
from rest_framework.exceptions import ValidationError

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


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=1, max_length=20)

class ProductValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=1, max_length=20)
    title = serializers.CharField(required=True, min_length=5, max_length=100)
    description = serializers.CharField(required=True, min_length=10, max_length=200)
    price = serializers.FloatField(required=True, min_value=1)

class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(required=True, min_length=10, max_length=200)
    prodict = serializers.IntegerField(required=True, min_value=1)
    stars = serializers.ChoiceField(choices=CHOICES, default=3)








