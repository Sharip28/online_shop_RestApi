from rest_framework import serializers

from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('image',)

    def _get_image_url(self,obj):
        request = self.context.get('request')
        if obj.image:
            url = obj.image.url
            if request is not None:
                url = request.build_absolute_uri(url)
            return url
        return ''

    def to_representation(self, instance):
        representation = super(ProductImageSerializer,self).to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class ProductSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    created = serializers.DateTimeField(format="%d %B %Y %H:%M", read_only=True)
    images = ProductImageSerializer(many=True,read_only=True)

    class Meta:
        model = Product
        # fields = ('id','name','price','category','description','status','created','images')
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        author = request.user
        # print(author)
        product = Product.objects.create(**validated_data,
            author=author
        )
        for image in images_data.getlist('images'):
            ProductImage.objects.create(product=product,
                                       image=image)
        return product

    def update(self,instance,validated_data):
        request = self.context.get('request')
        for key,value in validated_data.items():
            setattr(instance,key,value)
        instance.images.all().delete()
        images_data = request.FILES
        for image in images_data.getlist('images'):
            ProductImage.objects.create(
                product=instance,image=image
            )
        return instance

    def to_representation(self, instance):
        representation = super(ProductSerializer, self).to_representation(instance)
        representation['images'] = ProductImageSerializer(instance.images.all(),
                                                         many=True,context=self.context).data
        comments = CommentSerializer(instance.comments.all(), many=True).data
        likes = LikeSerializer(instance.likes.filter(like=True), many=True, context=self.context).data
        # representation['comments'] = len(comments)
        representation['likes'] = len(likes)
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data

        # representation['likes'] = LikeSerializer(instance.likes.filter(like=True), many=True, context=self.context).data

        return representation

    # def to_representation(self, instance):
    #     representation = super(ProductSerializer, self).to_representation(instance)
    #     action = self.context.get('action')
    #
    #     representation['images'] = ProductImageSerializer(instance.images.all(),
    #                                                      many=True,context=self.context).data
    #     comments = CommentSerializer(instance.comments.all(), many=True).data
    #     likes = LikeSerializer(instance.likes.filter(like=True), many=True, context=self.context).data
    #     if action == 'list':
    #         representation['comments'] = len(comments)
    #         representation['likes'] = len(likes)
    #     if action == 'detail':
    #         representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
    #         representation['likes'] = LikeSerializer(instance.likes.filter(like=True), many=True, context=self.context).data
    #
    #     return representation

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        comment = Comment.objects.create(author=author, **validated_data)
        return comment


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'product', 'user', 'like')

    def get_fields(self):
        action = self.context.get('action')
        fields = super().get_fields()
        if action == 'create':
            fields.pop('user')
            fields.pop('like')
        return fields

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        product = validated_data.get('product')
        like = Like.objects.get_or_create(user=user, product=product)[0]
        like.like = True if like.like is False else False
        like.save()
        return like

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['like'] = instance.like
        representation['user'] = instance.user.email
        return representation


class ParsSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    photo = serializers.CharField(max_length=255)
    price = serializers.CharField(max_length=100)