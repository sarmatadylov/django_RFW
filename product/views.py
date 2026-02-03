from re import search

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Avg
from .models import Category, Product, Review
from .serializers import CategorySerializer, CategoryDetailSerializer, ProductSerializer, ProductDetailSerializer
from .serializers import ReviewSerializer, ReviewDetailSerializer, ProductReviewSerializer

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
        category.name = request.data.get('name')
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
        name = request.data.get('name')

        category = Category.objects.create(name=name)
        return Response(status=status.HTTP_201_CREATED,
                        data= CategorySerializer(category).data)



@api_view(http_method_names=['GET'])
def product_list_api_view(request):
    if request.method == 'GET':
        search = request.query_params.get('search')

        if search:
            product = Product.objects.filter(name__icontains=search)


        data = ProductSerializer(product, many=True).data
        return Response(status=status.HTTP_200_OK, data=data)

    elif request.method == 'POST':
        name = request.data.get('name')
        title = request.data.get('title')
        price = request.data.get('price')
        description = request.data.get('description')
        category = request.data.get('category')

        product = Product.objects.create(name=name,
                                         title=title,
                                         description=description,
                                         price=price,
                                         category=category)
        return Response(status=status.HTTP_201_CREATED,
                        data= ProductSerializer(product).data)




@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductDetailSerializer(product).data
        return Response(data=data)
    elif request.method == 'PUT':
        product.name = request.data.get('name')
        product.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ProductSerializer(product).data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def review_list_api_view(request):
    if request.method == 'GET':
        search = request.query_params.get('search')

        if search:
            review = Review.objects.filter(name__icontains=search)



        data = ReviewSerializer(review, many=True).data
        return Response(status=status.HTTP_200_OK, data=data)

    elif request.method == 'POST':
        text = request.data.get('text')
        product = request.data.get('product')
        stars = request.data.get('stars')

        review = Review.objects.create(text=text,product=product,stars=stars)

    return Response(status=status.HTTP_201_CREATED,
                    data= ReviewSerializer(review).data)

@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewDetailSerializer(review).data
        return Response(data=data)
    elif request.method == 'PUT':
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








