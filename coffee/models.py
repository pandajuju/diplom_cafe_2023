from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.contrib.auth.models import User

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


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images', blank=True, null=True)

    def __str__(self):
        return self.title

    def snippet(self):
        return self.content[:100]

    @property
    def comments_count(self):
        return self.comments.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'


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
        ordering = ('-created_at', )


