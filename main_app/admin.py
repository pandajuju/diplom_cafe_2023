from django.contrib import admin
from .models import MainMenuItems


@admin.register(MainMenuItems)
class MainMenuItemsAdmin(admin.ModelAdmin):
    """
    Admin configuration for main menu items.

    Attributes:
        prepopulated_fields (dict): A dictionary specifying fields to be prepopulated based on other fields.
        list_display (tuple): A tuple specifying which fields to display in the list view of the admin interface.
        list_editable (tuple): A tuple specifying which fields to make editable in the list view of the admin interface.
    """
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'slug', 'is_anchor', 'is_visible', 'order')
    list_editable = ('is_anchor', 'is_visible', 'order')