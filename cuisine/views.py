from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Tag, Ingredient
from .serializers import TagSerializer, IngredientSerializer


class BaseAttributesViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Returns objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Creates a new attribute object"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseAttributesViewSet):
    """Manages tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(BaseAttributesViewSet):
    """Manages ingredients in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
