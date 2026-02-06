from re import search

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Avg
from .models import Category, Product, Review
from .serializers import CategorySerializer, CategoryDetailSerializer, ProductSerializer, ProductDetailSerializer
from .serializers import ReviewSerializer, ReviewDetailSerializer, ProductReviewSerializer, CategoryValidateSerializer,ProductValidateSerializer,ReviewValidateSerializer
from django.db import transaction

# Create your views here.

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
          data = CategoryDetailSerializer(category).data
          return Response(data=data)
    elif request.method == 'PUT':
        serializer = CategoryValidateSerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        category.name = serializer.validated_data.get('name')
        category.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=CategorySerializer(category).data)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(http_method_names=['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
         search = request.query_params.get('search')

         category = Category.objects.annotate(
               products_count=Count('products')
              )

         if search:
             category = category.filter(name__icontains=search)

         data = CategorySerializer(category, many=True).data
         return Response(status=status.HTTP_200_OK, data=data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)

        name = serializer.validated_data.get('name')

        with transaction.atomic():
            category = Category.objects.create(name=name)
            return Response(status=status.HTTP_201_CREATED,
                        data= CategorySerializer(category).data) 



@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        search = request.query_params.get('search')

        products = Product.objects

        if search:
            products = products.filter(name__icontains=search)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data.get('name')
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')

        with transaction.atomic():
            product = Product.objects.create(
                name=name,
                title=title,
                description=description,
                price=price
            )

        return Response(
            ProductSerializer(product).data,
            status=status.HTTP_201_CREATED
        )




@api_view(['GET' 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductDetailSerializer(product).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        product.name = request.data.get('name')
        product.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ProductSerializer(product).data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        search = request.query_params.get('search')

        reviews  = Review.objects

        if search:
            reviews = reviews.filter(name__icontains=search)

        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        text = serializer.validated_data.get('text')
        product = serializer.validated_data.get('product')
        stars = serializer.validated_data.get('stars')

        with transaction.atomic():
            review = Review.objects.create(
                text=text,
                product=product,
                stars=stars
            )
        return Response(
            ReviewSerializer(review).data,
            status=status.HTTP_201_CREATED,)





@api_view(['GET' 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewDetailSerializer(review).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializers = ReviewSerializer(review, data=request.data)
        serializers.is_valid(raise_exception=True)
        review.name = request.data.get('name')
        review.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=CategorySerializer(review).data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def product_reviews_api_view(request):
    products = Product.objects.annotate(
        rating=Avg('reviews__stars')
    ).prefetch_related('reviews')

    data = ProductReviewSerializer(products, many=True).data
    return Response(data, status=status.HTTP_200_OK)








