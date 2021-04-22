from django.db import models

# Create your models here.
from account.models import MyUser


class Category(models.Model):
    slug = models.SlugField(max_length=55,primary_key=True)
    name = models.CharField(max_length=55,unique=True)
    parent = models.ForeignKey('self',related_name='children',null=True,blank=True,on_delete=models.CASCADE)

    class Meta:
        ordering = ('slug',)

    def __str__(self):
        if self.parent:
            return f'{self.parent}->{self.name}'
        return self.name

    # @property
    # def get_children(self):
    #     if self.children:
    #         return self.children.all()
    #     return False

class Product(models.Model):
    CHOICES = (
        ('in stock', 'В наличии'),
        ('out of stock', 'Нет в наличии')
    )
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='products')

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(max_length=100, choices=CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('created',)


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products', blank=True, default='default.png')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
