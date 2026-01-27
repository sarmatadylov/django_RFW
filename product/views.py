from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import CategorySerializer, CategoryDetailSerializer, ProductSerializer, ProductDetailSerializer
from .serializers import ReviewSerializer, ReviewDetailSerializer

# Create your views here.

@api_view(['GET'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = CategoryDetailSerializer(category).data
    return Response(data=data)

@api_view(http_method_names=['GET'])
def category_list_api_view(request):
    category = Category.objects.all()
    print(category)

    data = CategorySerializer(category, many=True).data
    print(data)

    return Response(
        status=status.HTTP_200_OK,
        data=data
    )

@api_view(http_method_names=['GET'])
def product_list_api_view(request):
    product = Product.objects.all()
    print(product)

    data = ProductSerializer(product, many=True).data
    print(data)

    return Response(
        status=status.HTTP_200_OK,
        data=data
    )

@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = ProductDetailSerializer(product).data
    return Response(data=data)

@api_view(['GET'])
def review_list_api_view(request):
    review = Review.objects.all()
    print(review)

    data = ReviewSerializer(review, many=True).data
    print(data)

    return Response(
        status=status.HTTP_200_OK,
        data=data
    )
@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = ReviewDetailSerializer(review).data
    return Response(data=data)









