from typing import Dict

from .models import MainMenuItems


def main_menu_items(request) -> Dict[str, MainMenuItems]:
    """
    Retrieve main menu items for display.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        dict: A dictionary containing the main menu items.
    """
    items = MainMenuItems.objects.filter(is_visible=True)
    return {'main_menu': items}
