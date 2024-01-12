from django.contrib import admin
from .models import DishCategory, Dish, Post, Comment, PostCategory, Tag, PostImage, Reservation
from django.utils.safestring import mark_safe


admin.site.register(Reservation)
admin.site.register(DishCategory)
admin.site.register(PostCategory)
# admin.site.register(Tag)
admin.site.register(PostImage)


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


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag


class PostImageInline(admin.TabularInline):
    model = PostImage


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted', 'category', 'get_tags', 'get_images')
    search_fields = ['title', 'content']
    list_filter = ('date_posted', 'author')

    def get_tags(self, obj):
        return ", ".join([tag.tag_name for tag in obj.tags.all()])

    def get_images(self, obj):
        return ", ".join([str(image) for image in obj.postimage_set.all()])

    get_tags.short_description = 'Tags'
    get_images.short_description = 'Images'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'author', 'date_posted', 'email', 'parent_id',)
    search_fields = ['content']
    list_filter = ('date_posted', 'author')
