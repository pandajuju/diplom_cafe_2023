import uuid

from ckeditor.fields import RichTextField
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils.html import strip_tags


class DishCategory(models.Model):
    """
    Model representing a category for dishes.

    Attributes:
        name (str): The name of the dish category.
        order (int): The order of the dish category.
        is_visible (bool): Indicates if the dish category is visible.
    """
    name = models.CharField(max_length=255, unique=True, db_index=True)
    order = models.PositiveSmallIntegerField()
    is_visible = models.BooleanField(default=True)

    def __iter__(self):
        """
        Iterates over visible dishes in the category.

        Yields:
            Dish: A visible dish in the category.
        """
        dishes = self.dishes.filter(is_visible=True)
        for dish in dishes:
            yield dish

    class Meta:
        """
        Metaclass for defining model metadata.

        Attributes:
            verbose_name_plural (str): The plural name for the model in the admin interface.
            ordering (tuple): The default ordering for queries.
        """
        verbose_name_plural = 'Dish Categories'
        ordering = ('order',)

    def __str__(self) -> str:
        """
         Returns the string representation of the dish category.

        Returns:
            str: The name of the dish category.
        """
        return f'{self.name}'


class Dish(models.Model):
    """
    Model representing a dish.

    Attributes:
        name (str): The name of the dish.
        slug (str): The slug for the URL.
        description (str): The description of the dish.
        price (Decimal): The price of the dish.
        photo (ImageField): The photo of the dish.
        is_visible (bool): Indicates if the dish is visible.
        order (int): The order of the dish.
        category (DishCategory): The category to which the dish belongs.
    """
    name = models.CharField(max_length=255, unique=True, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='url')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    photo = models.ImageField(upload_to='dishes/', blank=True)
    is_visible = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField()

    category = models.ForeignKey(DishCategory, on_delete=models.PROTECT, related_name='dishes')

    def __str__(self):
        """
        Returns the string representation of the dish.

        Returns:
            str: The name of the dish.
        """
        return self.name


class Gallery(models.Model):
    """
    Model representing a gallery item.

    Attributes:
        photo (ImageField): The photo of the gallery item.
        is_visible (bool): Indicates if the gallery item is visible.
        title (str): The title of the gallery item.
    """
    photo = models.ImageField(upload_to='gallery/')
    is_visible = models.BooleanField(default=True)
    title = models.CharField(max_length=255, blank=True)


class PostCategory(models.Model):
    """
    Model representing a category for posts.

    Attributes:
        name (str): The name of the post category.
    """
    name = models.CharField(max_length=200, unique=True, db_index=True)

    def __iter__(self):
        """
        Iterates over posts in the category.

        Yields:
            Post: A post in the category.
        """
        posts = self.posts.all()
        for post in posts:
            yield post

    class Meta:
        """
        Metaclass for defining model metadata.

        Attributes:
            verbose_name_plural (str): The plural name for the model in the admin interface.
        """
        verbose_name_plural = 'Post Categories'

    def __str__(self) -> str:
        """
        Returns the string representation of the post category.

        Returns:
            str: The name of the post category.
        """
        return f'{self.name}'


class Tag(models.Model):
    """
    Model representing a tag for posts.

    Attributes:
        tag_name (str): The name of the tag.
    """
    tag_name = models.CharField(max_length=50, unique=True, db_index=True)

    class Meta:
        """
        Metaclass for defining model metadata.

        Attributes:
            ordering (list): The default ordering for queries.
        """
        ordering = ["tag_name"]

    def __str__(self) -> str:
        """
        Returns the string representation of the tag.

        Returns:
            str: The name of the tag.
        """
        return self.tag_name


class Post(models.Model):
    """
    Model representing a blog post.

    Attributes:
        title (str): The title of the post.
        content (RichTextField): The content of the post.
        date_posted (datetime): The date and time when the post was created.
        author (User): The author of the post.
        is_visible (bool): Indicates if the post is visible.
        tags (QuerySet): The tags associated with the post.
        category (PostCategory): The category to which the post belongs.
    """
    title = models.CharField(max_length=200, unique=True, db_index=True)
    content = RichTextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_visible = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag)

    category = models.ForeignKey(PostCategory, on_delete=models.PROTECT, related_name='posts', default=1, null=True)

    def truncated_content(self) -> str:
        """
        Returns a truncated version of the post content.

        Returns:
            str: The truncated content.
        """
        content_without_tags = strip_tags(self.content)
        return content_without_tags[:150]

    def __str__(self) -> str:
        """
        Returns the string representation of the post.

        Returns:
            str: The title of the post.
        """
        return self.title

    def snippet(self) -> str:
        """
        Returns a snippet of the post content.

        Returns:
            str: The snippet of the content.
        """
        return self.content[:100]

    @property
    def comments_count(self) -> int:
        """
        Returns the count of comments for the post.

        Returns:
            int: The number of comments.
        """
        return self.comments.count()


class PostImage(models.Model):
    """
    Model representing an image associated with a post.

    Attributes:
        post_image (ImageField): The image file associated with the post.
        post (Post): The post to which the image belongs.
    """
    post_image = models.ImageField(upload_to='post_images')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """
        Returns the string representation of the post image.

        Returns:
            str: A descriptive string for the post image.
        """
        return f"Image {self.pk}"


class Comment(models.Model):
    """
    Model representing a comment on a post.

    Attributes:
        post (Post): The post to which the comment belongs.
        content (str): The content of the comment.
        email (str): The email address of the commenter.
        date_posted (datetime): The date and time when the comment was posted.
        author (str): The name of the commenter.
        parent (Comment): The parent comment if this is a reply, None otherwise.
    """
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    email = models.EmailField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.TextField()
    parent = models.ForeignKey('self', related_name='replies', on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        """
        Returns the string representation of the comment.

        Returns:
            str: A descriptive string for the comment.
        """
        return f'Comment by {self.author} on {self.post.title}'


class Reservation(models.Model):
    """
    Model representing a reservation.

    Attributes:
        name (str): The first name of the person making the reservation.
        last_name (str): The last name of the person making the reservation.
        date (Date): The date of the reservation.
        time (Time): The time of the reservation.
        phone (str): The phone number of the person making the reservation.
        message (str): Any additional message associated with the reservation.
        is_processed (bool): Indicates if the reservation has been processed.
        created_at (DateTime): The date and time when the reservation was created.
        updated_at (DateTime): The date and time when the reservation was last updated.
    """
    name = models.CharField(max_length=100, unique=True, db_index=True)
    last_name = models.CharField(max_length=100, unique=True, db_index=True)
    date = models.DateField()
    time = models.TimeField()
    phone_regex = RegexValidator(regex=r'^\+?\d{7,12}$',
                                 message='Phone number should be in format: +380xxxxxxxxx')
    phone = models.CharField(validators=[phone_regex, ], max_length=20)
    message = models.TextField(max_length=500, blank=True, unique=True, db_index=True)

    is_precessed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """
        Returns the string representation of the reservation.

        Returns:
            str: The string representation of the reservation.
        """
        return f'{self.name} - {self.phone}'

    class Meta:
        """
        Metaclass for defining model metadata.

        Attributes:
            ordering (tuple): The default ordering for queries.
        """
        ordering = ('-created_at',)


class Order(models.Model):
    """
    Model representing an order.

    Attributes:
        order_id (UUID): The unique identifier for the order.
        order_date (Date): The date when the order was placed.
        order_time (Time): The time when the order was placed.
        order_status (str): The status of the order.
    """
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    order_date = models.DateField(auto_now_add=True)
    order_time = models.TimeField(auto_now_add=True)
    order_status = models.CharField(max_length=100)

    def __str__(self) -> str:
        """
        Returns the string representation of the order.

        Returns:
            str: The string representation of the order.
        """
        return f"Order {self.order_id} - {self.order_date} {self.order_time}"


class UserData(models.Model):
    """
    Model representing user data for orders.

    Attributes:
        user (User): The user associated with the data.
        order (Order): The order related to the user data.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        street_name (str): The street name of the user's address.
        house_number (str): The house number of the user's address.
        phone (str): The phone number of the user.
        email_address (str): The email address of the user.
        is_completed (bool): Indicates if the user data is completed.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street_name = models.CharField(max_length=255)
    house_number = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    email_address = models.EmailField()
    is_completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        """
        Returns a string representation of the user data.

        Returns:
            str: A string containing the username and order ID.
        """
        user_username = getattr(self.user, 'username', 'Unknown User')
        return f"{user_username} - Order {self.order.order_id}"


class OrderDishesList(models.Model):
    """
    Model representing the list of dishes in an order.

    Attributes:
        order (Order): The order associated with the list of dishes.
        user_data (UserData): The user data related to the order.
        dish (Dish): The dish included in the order.
        price (Decimal): The price of the dish.
        quantity (int): The quantity of the dish in the order.
    """
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    user_data = models.ForeignKey(UserData, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        """
        Returns a string representation of the order dish list entry.

        Returns:
            str: A string containing the order ID and dish name.
        """
        return f"{self.order} - {self.dish.name}"



