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
    created = serializers.DateTimeField(format="%d %B %Y %H:%M", read_only=True)
    images = ProductImageSerializer(many=True,read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(ProductSerializer,self).to_representation(instance)
        # representation['images'] = ProductImageSerializer(instance.images.all(),
        #                                                  many=True,context=self.context).data
        return representation



