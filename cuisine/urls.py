from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('tag', views.TagViewSet)
router.register('ingredient', views.IngredientViewSet)
app_name = 'cuisine'

urlpatterns = [
    path('', include(router.urls)),
]
