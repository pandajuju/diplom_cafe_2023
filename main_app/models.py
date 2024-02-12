from django.db import models
from django.urls import reverse


class MainMenuItems(models.Model):
    """
    Model representing the main menu items.

    Attributes:
        title (str): The title of the menu item.
        slug (str): The slug for the URL.
        url (str): The URL for the menu item.
        is_anchor (bool): Indicates if the menu item is an anchor link.
        is_manager_only (bool): Indicates if the menu item is visible only to managers.
        is_visible (bool): Indicates if the menu item is visible.
        order (int): The order of the menu item.
    """
    title = models.CharField(max_length=50, verbose_name='menu item')
    slug = models.SlugField(max_length=50, db_index=True, verbose_name='url')
    url = models.CharField(max_length=100, blank=True)
    is_anchor = models.BooleanField(default=False)
    is_manager_only = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField()

    def get_absolute_url(self) -> str:
        """
          Returns the absolute URL for the menu item.

          Returns:
              str: The absolute URL.
        """
        if self.is_anchor:
            return reverse('coffee:home') + f'#{self.slug}'
        return self.url

    def __str__(self) -> str:
        """
        Returns a string representation of the menu item.

        Returns:
            str: The string representation.
        """
        return f'{self.title}/{self.slug}'

    class Meta:
        ordering = ('order',)
