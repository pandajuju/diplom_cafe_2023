from django.test import TestCase
from .models import MainMenuItems


class MainMenuItemsTestCase(TestCase):
    """
    Test case for MainMenuItems model.

    Methods:
        setUp(): Set up method for creating test data.
        test_menu_item_creation(): Test method for creating a main menu item.
        test_get_absolute_url(): Test method for getting the absolute URL of a main menu item.
        test_string_representation(): Test method for string representation of a main menu item.
    """
    def setUp(self) -> None:
        self.menu_item = MainMenuItems.objects.create(
            title='Test Item',
            slug='test-item',
            url='/test/',
            is_anchor=False,
            is_manager_only=False,
            is_visible=True,
            order=1
        )

    def test_menu_item_creation(self) -> None:
        self.assertEqual(self.menu_item.title, 'Test Item')
        self.assertEqual(self.menu_item.slug, 'test-item')
        self.assertEqual(self.menu_item.url, '/test/')
        self.assertFalse(self.menu_item.is_anchor)
        self.assertFalse(self.menu_item.is_manager_only)
        self.assertTrue(self.menu_item.is_visible)
        self.assertEqual(self.menu_item.order, 1)

    def test_get_absolute_url(self):
        self.assertEqual(self.menu_item.get_absolute_url(), '/test/')

    def test_string_representation(self):
        self.assertEqual(str(self.menu_item), 'Test Item/test-item')
