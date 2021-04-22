from django.contrib import admin
from django.contrib.admin import ModelAdmin
from main.models import *


admin.site.register(Category)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    max_num = 10
    min_num = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ]