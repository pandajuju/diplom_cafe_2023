from ckeditor.fields import RichTextField
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils.html import strip_tags


class DishCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    order = models.PositiveSmallIntegerField()
    is_visible = models.BooleanField(default=True)

    def __iter__(self):
        dishes = self.dishes.filter(is_visible=True)
        for dish in dishes:
            yield dish

    class Meta:
        verbose_name_plural = 'Dish Categories'
        ordering = ('order',)

    def __str__(self):
        return f'{self.name}'


class Dish(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='url')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='dishes/', blank=True)
    is_visible = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField()

    category = models.ForeignKey(DishCategory, on_delete=models.PROTECT, related_name='dishes')


class Gallery(models.Model):
    photo = models.ImageField(upload_to='gallery/')
    is_visible = models.BooleanField(default=True)
    title = models.CharField(max_length=255, blank=True)


class PostCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __iter__(self):
        posts = self.posts.all()
        for post in posts:
            yield post

    class Meta:
        verbose_name_plural = 'Post Categories'

    def __str__(self):
        return f'{self.name}'


class Tag(models.Model):
    tag_name = models.CharField(max_length=50)

    class Meta:
        ordering = ["tag_name"]

    def __str__(self):
        return self.tag_name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_visible = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag)

    category = models.ForeignKey(PostCategory, on_delete=models.PROTECT, related_name='posts', default=1, null=True)

    def truncated_content(self):
        content_without_tags = strip_tags(self.content)
        return content_without_tags[:150]

    def __str__(self):
        return self.title

    def snippet(self):
        return self.content[:100]

    @property
    def comments_count(self):
        return self.comments.count()


class PostImage(models.Model):
    post_image = models.ImageField(upload_to='post_images')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"Image {self.pk}"


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    email = models.EmailField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.TextField()
    parent = models.ForeignKey('self', related_name='replies', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post.title}'


class Reservation(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    phone_regex = RegexValidator(regex=r'^\+?\d{7,12}$',
                                 message='Phone number should be in format: +380xxxxxxxxx')
    phone = models.CharField(validators=[phone_regex, ], max_length=20)
    message = models.TextField(max_length=500, blank=True)

    is_precessed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.phone}'

    class Meta:
        ordering = ('-created_at',)


class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street_name = models.CharField(max_length=255)
    house_number = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    email_address = models.EmailField()


class OrderDishesList(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.order} - {self.dish.name}"


class Order(models.Model):
    order_date = models.DateField(auto_now_add=True)
    order_time = models.TimeField(auto_now_add=True)
    order_status = models.CharField(max_length=100)


