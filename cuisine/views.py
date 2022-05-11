from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Tag, Ingredient, Recipe
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer, RecipeDetailSerializer, RecipeImageSerializer


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


class RecipeViewSet(viewsets.ModelViewSet):
    """Manages recipes in the database"""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Returns objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Returns the appropriate serializer class"""
        if self.action == 'retrieve':
            return RecipeDetailSerializer
        elif self.action == 'upload_image':
            return RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Creates a new recipe object"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Uploads an image to a recipe"""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
