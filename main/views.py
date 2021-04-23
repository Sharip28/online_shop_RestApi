from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, viewsets, status, mixins
from rest_framework.decorators import api_view, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Product, ProductImage, Comment, Like
from .permissions import IsAuthorPermission
from .serializers import CategorySerializer, ProductSerializer, ProductImageSerializer, CommentSerializer, \
    LikeSerializer, ParsSerializer
from .utils import parsing


# class MyPaginationClass(PageNumberPagination):
#     page_size = 2
#
#     def get_paginated_response(self, data):
#         for i in range(self.page_size):
#             text = data[i]['description']
#             data[i]['description'] = text[:15] + '...'
#             likes = data[i]['likes']
#             data[i]['likes'] = len(likes)
#             comments = data[i]['comments']
#             data[i]['comments'] = len(comments)
#             # data[i]['recommends'] = len(data[i]['recommends'])
#         return super().get_paginated_response(data)
#

class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated,]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission, IsAuthenticated]
        else:
            permissions = []
        return [permission() for permission in permissions]


class PermissionMixinComment:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated, ]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission, IsAuthenticated]
        else:
            permissions = []
        return [permission() for permission in permissions]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(PermissionMixin,viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # pagination_class = MyPaginationClass


    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(name__icontains=q) |
                                   Q(description__icontains=q))
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def sort(self, request):
        filter = request.query_params.get('filter')
        if filter == 'A-Z':
            queryset = self.get_queryset().order_by('name')
        elif filter == 'Z-A':
            queryset = self.get_queryset().order_by('-name')

        else:
            queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(PermissionMixinComment,viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticated, ]


class ParsingView(APIView):
    def get(self, request):
        dict_ = parsing()
        serializer = ParsSerializer(instance=dict_, many=True)
        return Response(serializer.data)


class LikeViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}




class ProoductImageView(generics.ListAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}
