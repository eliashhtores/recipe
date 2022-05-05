from django.contrib import admin
from .models import Tag, Ingredient, Recipe


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_minutes', 'price', 'link')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'tags', 'ingredients')
    list_filter = ('tags', )


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
