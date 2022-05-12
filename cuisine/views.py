"""Views for the Cuisine app."""
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Tag, Ingredient, Recipe
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer, RecipeDetailSerializer, RecipeImageSerializer


class BaseAttributesViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Generic class to be used by tags and ingredients"""
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Returns objects for the current authenticated user only"""
        assigned_only = bool(int(self.request.GET.get('assigned_only', 0)))
        queryset = self.queryset

        if assigned_only:
            queryset = self.queryset.filter(recipe__isnull=False)
        return queryset.filter(user=self.request.user).order_by('-name').distinct()

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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self, qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Returns objects for the current authenticated user only"""
        tags = self.request.GET.get('tags')
        ingredients = self.request.GET.get('ingredients')
        queryset = self.queryset

        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = self.queryset.filter(tags__id__in=tag_ids).distinct()

        if ingredients:
            ingredients_ids = self._params_to_ints(ingredients)
            queryset = self.queryset.filter(
                ingredients__id__in=ingredients_ids
            ).distinct()

        return queryset.filter(user=self.request.user).order_by('-id')

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
