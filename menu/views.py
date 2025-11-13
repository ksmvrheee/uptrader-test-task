from django.shortcuts import render


def show_menu_example(request):
    """
    Displays a nested menu on the example page using the
    'draw_menu' template tag from 'menu_tags'. Query params
    'menu' and 'item' are expected specifying the exact label
    of the desired menu(s) and the exact item url from the database.
    """
    menu_types = request.GET.getlist('menu')
    item_url = request.GET.get('item_url', '#')

    return render(
        request, 'menu/example.html',
        {'menu_types': menu_types}
    )

    # the following request is expected: /?menu=main_menu&menu=secondary_menu&item_url=computers,
    # or just: /?menu=main_menu&item_url=computers or /?menu=main_menu
