from rest_framework import serializers
from .models import Category, Product, Review
from django.db.models import Avg
from rest_framework.exceptions import ValidationError

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

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
        fields = ['id', 'text', 'stars']


class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'reviews', 'rating']

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('stars'))['stars__avg']


class CategoryWithCountSerialzier(serializers.ModelSerializer):
    products_count = serializers.IntegerField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']


class ProductValidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category']

    def create(self, validated_data):
        # owner автоматически берём из request.user
        validated_data['owner'] = self.context['request'].user
        return Product.objects.create(**validated_data)

    def validate_category(self, value):
        if not Category.objects.filter(id=value.id).exists():
            raise ValidationError('Category does not exist!')
        return value


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField()


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(required=False)
    product = serializers.IntegerField()
    stars = serializers.FloatField(min_value=1, max_value=11)

    def validate(self, attrs):
        product = attrs['product']
        if not Product.objects.filter(id=product).exists():
            raise ValidationError('Product does not exist!')
        return attrs