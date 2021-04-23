"""hackathon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cart.views import CartViewSet
from hackathon import settings
from main.views import ProductViewSet, CategoryListView, CommentViewSet, LikeViewSet

router = DefaultRouter()
router.register('products',ProductViewSet)
router.register('comments', CommentViewSet)
router.register('likes', LikeViewSet)
router.register('cart', CartViewSet)





urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/api/account/', include('account.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('v1/api/categories/',CategoryListView.as_view()),
    path('v1/api/',include(router.urls)),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)