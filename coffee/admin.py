from django.contrib import admin
from .models import DishCategory, Dish, Post, Comment, Reservation
from django.utils.safestring import mark_safe

# Register your models here.
admin.site.register(Reservation)
admin.site.register(DishCategory)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'category', 'name', 'price', 'is_visible', 'photo_src_tag')
    list_editable = ('category', 'name', 'price', 'is_visible')
    search_fields = ('name',)
    list_filter = ('category', 'price', 'is_visible')

    def photo_src_tag(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width=50>")

    photo_src_tag.short_description = 'Dish photo'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted')
    search_fields = ['title', 'content']
    list_filter = ('date_posted', 'author')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'date_posted')
    search_fields = ['content']
    list_filter = ('date_posted', 'author')
