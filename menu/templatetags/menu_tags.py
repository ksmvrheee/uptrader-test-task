from django import template

from ..utils import MenuBuilder

register = template.Library()


@register.inclusion_tag('menu/draw_menu.html', takes_context=True)
def draw_menu(context, desired_type):
    """
    Inclusion tag to draw a nested menu utilizing the MenuBuilder
    class and the corresponding model. Obtains the current selected item URL,
    current menu type/label and a list of menu types from the current GET-query params.
    """
    builder = MenuBuilder(
        item_url=context.request.GET.get('item_url'),
        menu_type=desired_type,
        menu_types=context.request.GET.getlist('menu')
    )
    menu_items = builder.get_result()

    return {'menu_items': menu_items}
