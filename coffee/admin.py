from django.contrib import admin
from .models import DishCategory, Dish, Post, Comment, PostCategory, Tag, PostImage, Reservation, OrderDishesList, \
    Order, UserData
from django.utils.safestring import mark_safe


admin.site.register(Reservation)
admin.site.register(DishCategory)
admin.site.register(PostCategory)
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


# @admin.register(OrderDishesList)
# class OrderDishesListAdmin(admin.ModelAdmin):
#     list_display = ['order_id', 'user', 'dish', 'price', 'quantity']
#     search_fields = ['user__username', 'dish__name']
#
#
# @admin.register(UserData)
# class UserDataAdmin(admin.ModelAdmin):
#     list_display = ['user', 'first_name', 'last_name', 'street_name', 'house_number', 'phone', 'email_address']
#     search_fields = ['user__username', 'first_name', 'last_name', 'email_address']
#
#
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['user_data', 'order_date', 'order_time', 'order_status']
#     search_fields = ['user_data__user__username', 'order_status']
#     filter_horizontal = ['order_dishes_list']

@admin.register(OrderDishesList)
class OrderDishesListAdmin(admin.ModelAdmin):
    list_display = ['dish', 'price', 'quantity']
    search_fields = ['dish__name']


@admin.register(UserData)
class UserDataAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'street_name', 'house_number', 'phone', 'email_address']
    search_fields = ['first_name', 'last_name', 'email_address']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_date', 'order_time', 'order_status']
    search_fields = ['order_status']
    # filter_horizontal = ['order_dishes_list']
