import uuid
from datetime import time
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.contrib.auth.models import User
from django.test import TestCase
from coffee.models import Dish, DishCategory, PostCategory, Gallery, Tag, Post, Order, Reservation, Comment, PostImage, \
    UserData


class DishCategoryTestCase(TestCase):
    """
    Test case for DishCategory model.

    Methods:
        setUp(): Sets up the test environment by creating a DishCategory instance.
        test_category_creation(): Tests the creation of a DishCategory instance.
        test_dishes_iteration(): Tests the iteration over dishes in the category.
        test_str_representation(): Tests the string representation of a DishCategory instance.
    """
    def setUp(self) -> None:
        self.category = DishCategory.objects.create(name='Test Category', order=1)

    def test_category_creation(self) -> None:
        self.assertEqual(self.category.name, 'Test Category')
        self.assertEqual(self.category.order, 1)
        self.assertTrue(self.category.is_visible)

    def test_dishes_iteration(self) -> None:
        dish = Dish.objects.create(name='Test Dish', slug='test-dish', description='Test description',
                                   price=10.00, order=1, category=self.category)

        dishes = list(self.category)
        self.assertIn(dish, dishes)

    def test_str_representation(self) -> None:
        self.assertEqual(str(self.category), 'Test Category')


class DishTestCase(TestCase):
    """
    Test case for Dish model.

    Methods:
        setUp(): Sets up the test environment by creating a DishCategory and a Dish instance.
        test_dish_creation(): Tests the creation of a Dish instance.
        test_str_representation(): Tests the string representation of a Dish instance.
    """
    def setUp(self) -> None:
        self.category = DishCategory.objects.create(name='Test Category', order=1)
        self.dish = Dish.objects.create(name='Test Dish', slug='test-dish', description='Test description', price=10.00,
                                        order=1, category=self.category)

    def test_dish_creation(self) -> None:
        self.assertEqual(self.dish.name, 'Test Dish')
        self.assertEqual(self.dish.slug, 'test-dish')
        self.assertEqual(self.dish.description, 'Test description')
        self.assertEqual(self.dish.price, 10.00)
        self.assertTrue(self.dish.is_visible)
        self.assertEqual(self.dish.order, 1)
        self.assertEqual(self.dish.category, self.category)

    def test_str_representation(self) -> None:
        self.assertEqual(str(self.dish), 'Test Dish')


class GalleryTestCase(TestCase):
    """
    Test case for the Gallery model.

    Methods:
        setUp(): Set up initial data for tests.
        test_gallery_item_creation(): Test creation of a gallery item.
    """
    def setUp(self) -> None:
        self.gallery_item = Gallery.objects.create(photo='test.jpg', title='Test Gallery Item')

    def test_gallery_item_creation(self) -> None:
        self.assertEqual(self.gallery_item.photo, 'test.jpg')
        self.assertEqual(self.gallery_item.title, 'Test Gallery Item')
        self.assertTrue(self.gallery_item.is_visible)


class PostCategoryTestCase(TestCase):
    """
    Test case for the PostCategory model.

    Methods:
        setUp(): Set up initial data for tests.
        test_category_creation(): Test creation of a post category.
        test_str_representation(): Test string representation of a post category.
    """
    def setUp(self) -> None:
        self.category = PostCategory.objects.create(name='Test Post Category')

    def test_category_creation(self) -> None:
        self.assertEqual(self.category.name, 'Test Post Category')

    def test_str_representation(self) -> None:
        self.assertEqual(str(self.category), 'Test Post Category')


class TagTestCase(TestCase):
    """
    Test case for the Tag model.

    Methods:
        setUp(): Set up initial data for tests.
        test_tag_creation(): Test creation of a tag.
        test_str_representation(): Test string representation of a tag.
    """
    def setUp(self) -> None:
        self.tag = Tag.objects.create(tag_name='Test Tag')

    def test_tag_creation(self) -> None:
        self.assertEqual(self.tag.tag_name, 'Test Tag')

    def test_str_representation(self) -> None:
        self.assertEqual(str(self.tag), 'Test Tag')


class PostTestCase(TestCase):
    """
    Test case for the Post model.

    Methods:
        setUp(): Set up the test environment.
        test_post_creation(): Test post creation.
        test_truncated_content(): Test truncated_content method of Post.
        test_str_representation(): Test string representation of Post.
        test_snippet(): Test snippet method of Post.
        test_comments_count(): Test comments_count method of Post.
    """
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.category = PostCategory.objects.create(name='Test Post Category')
        self.post = Post.objects.create(title='Test Post',
                                        content='Test Content', author=self.user, category=self.category)

    def test_post_creation(self) -> None:
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.content, 'Test Content')
        self.assertTrue(self.post.date_posted <= timezone.now())
        self.assertEqual(self.post.author, self.user)
        self.assertTrue(self.post.is_visible)
        self.assertEqual(self.post.category, self.category)

    def test_truncated_content(self) -> None:
        truncated_content = self.post.truncated_content()
        self.assertEqual(truncated_content, 'Test Content')

    def test_str_representation(self) -> None:
        self.assertEqual(str(self.post), 'Test Post')

    def test_snippet(self) -> None:
        snippet = self.post.snippet()
        self.assertEqual(snippet, 'Test Content')

    def test_comments_count(self) -> None:
        self.post.comments.create(author=self.user, content='Comment 1')
        self.post.comments.create(author=self.user, content='Comment 2')

        self.assertEqual(self.post.comments_count, 2)


class PostImageTestCase(TestCase):
    """
    Test case for the PostImage model.

    Methods:
        setUp(): Set up data for testing.
        test_post_image_created(): Test if a PostImage instance is created successfully.
        test_post_image_str_method(): Test the __str__() method of PostImage model.
        test_post_image_deletion(): Test deletion of associated PostImage instance when its related Post is deleted.
    """
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="test_user", password="test_password")
        category = PostCategory.objects.create(name="Test Category")
        self.post = Post.objects.create(title="Test Post", content="Test content", category=category, author=self.user)
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        self.post_image = PostImage.objects.create(post=self.post, post_image=image)

    def test_post_image_created(self) -> None:
        self.assertEqual(self.post_image.post, self.post)
        self.assertTrue(self.post_image.post_image)

    def test_post_image_str_method(self) -> None:
        expected_string = f"Image {self.post_image.pk}"
        self.assertEqual(str(self.post_image), expected_string)

    def test_post_image_deletion(self) -> None:
        post_id = self.post.id
        self.post.delete()
        self.assertFalse(PostImage.objects.filter(post_id=post_id).exists())


class CommentTestCase(TestCase):
    """
    Test case for the Comment model.

    Methods:
        setUp(): Set up data for testing.
        test_comment_creation(): Test if a Comment instance is created successfully.
        test_str_representation(): Test the __str__() method of Comment model.
    """
    def setUp(self) -> None:
        category = PostCategory.objects.create(name="Test Category")
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='test_password')
        self.post = Post.objects.create(title='Test Post', content='Test Content', category=category, author=self.user)
        self.comment = Comment.objects.create(post=self.post, content='Test Comment',
                                              email='test@example.com', author='Test Author')

    def test_comment_creation(self) -> None:
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.content, 'Test Comment')
        self.assertEqual(self.comment.email, 'test@example.com')
        self.assertEqual(self.comment.author, 'Test Author')
        self.assertIsNotNone(self.comment.date_posted)

    def test_str_representation(self) -> None:
        self.assertEqual(str(self.comment), 'Comment by Test Author on Test Post')


class ReservationTestCase(TestCase):
    """
    Test case for Reservation model.

    Methods:
        test_reservation_creation(): Test method for creating a reservation.
        test_str_representation(): Test method for string representation of a reservation.
    """
    def test_reservation_creation(self) -> None:
        now_time = timezone.now().time()
        reservation = Reservation.objects.create(name='John', last_name='Doe', date=timezone.now().date(),
                                                 time=timezone.now().time(), phone='+380123456789')
        self.assertEqual(reservation.name, 'John')
        self.assertEqual(reservation.last_name, 'Doe')
        self.assertEqual(reservation.date, timezone.now().date())
        rounded_db_time = time(reservation.time.hour, reservation.time.minute, reservation.time.second)
        rounded_now_time = time(now_time.hour, now_time.minute, now_time.second)
        self.assertEqual(rounded_db_time, rounded_now_time)
        self.assertEqual(reservation.phone, '+380123456789')

    def test_str_representation(self) -> None:
        now_time = timezone.now().time()
        reservation = Reservation.objects.create(name='John', last_name='Doe', date=timezone.now().date(),
                                                 time=now_time, phone='+380123456789')
        self.assertEqual(str(reservation), 'John - +380123456789')


class OrderTestCase(TestCase):
    """
    Test case for Order model.

    Methods:
        test_order_creation(): Test method for creating an order.
        test_str_representation(): Test method for string representation of an order.
    """
    def test_order_creation(self) -> None:
        order = Order.objects.create(order_status='Pending')
        self.assertTrue(order.order_id)
        self.assertEqual(order.order_status, 'Pending')

    def test_str_representation(self) -> None:
        order = Order.objects.create(order_status='Pending')
        self.assertEqual(str(order), f'Order {order.order_id} - {order.order_date} {order.order_time}')


class UserDataTestCase(TestCase):
    """
    Test case for UserData model.

    Methods:
        setUp(): Set up method for creating test data.
        test_user_data_creation(): Test method for creating user data.
        test_str_representation(): Test method for string representation of user data.
    """
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.order = Order.objects.create(order_status='Pending')
        self.user_data = UserData.objects.create(user=self.user, order=self.order, first_name='John',
                                                 last_name='Doe', street_name='Main St', house_number='123',
                                                 phone='+380123456789', email_address='john@example.com')

    def test_user_data_creation(self) -> None:
        self.assertEqual(self.user_data.user, self.user)
        self.assertEqual(self.user_data.order, self.order)
        self.assertEqual(self.user_data.first_name, 'John')
        self.assertEqual(self.user_data.last_name, 'Doe')
        self.assertEqual(self.user_data.street_name, 'Main St')
        self.assertEqual(self.user_data.house_number, '123')
        self.assertEqual(self.user_data.phone, '+380123456789')
        self.assertEqual(self.user_data.email_address, 'john@example.com')
        self.assertFalse(self.user_data.is_completed)

    def test_str_representation(self) -> None:
        self.assertEqual(str(self.user_data), f"{self.user.username} - Order {self.order.order_id}")

