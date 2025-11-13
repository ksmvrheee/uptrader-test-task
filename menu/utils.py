from collections import defaultdict

from django.apps import apps


class MenuBuilder:
    """
    A class to build html code for a menu from the model in the database.

    This class takes a unique menu label (type), a current item URL and types
    of the menus mentioned in the initial request, iterates the elements and
    returns an unfolded menu with the elements being links for the items. It uses
    a tree-like structure to organize the menu items, supporting complex structure.
    """
    def __init__(self, item_url: str, menu_type: str, menu_types: list[str]):
        """
        Initializes the MenuBuilder with the given parameters.

        :param item_url: the URL of the current selected menu item.
        :param menu_type: the label (type) of a menu to build.
        :param menu_types: a list of menu types from the current request to consider.
        """
        self.item_url = item_url
        self.menu_types = menu_types
        self.menu_models_registry = self.build_menu_models_registry()
        self.model = self.resolve_model(menu_type)
        self.query = self.build_query()
        self.items = list(self.model.objects.all())

        self.tree = defaultdict(list)
        self.build_tree()

    @staticmethod
    def build_menu_models_registry() -> dict:
        """
        Composes a dictionary from this app's models containing the menu
        models labels as keys and model objects themselves as values.
        """
        return {
            model.menu_label: model
            for model in apps.get_app_config('menu').get_models()
            if hasattr(model, 'menu_label')
        }

    def resolve_model(self, menu_type: str):
        """
        Resolves the model by it's type/label that must present in every menu model.
        If there is not a single model with this type, raises ValueError.
        """
        menu_model = self.menu_models_registry.get(menu_type)

        if menu_model is not None:
            return menu_model
        else:
            raise ValueError(f'Unknown menu type: "{menu_type}".')

    def build_query(self):
        """Restores an initial query preserving all mentioned menus."""
        return f'?{"&".join(map(lambda x: "menu=" + x, self.menu_types))}&item_url='

    def build_tree(self):
        """
        Builds the tree dict representing the hierarchical menu itself with the
        keys being "parent elements" and the values being "children elements".
        """
        for item in self.items:
            self.tree[item.parent_id].append(item)

    def add_descendants_to_processed(self, item, processed):
        """Recursively adds descendants of an item to the processed set."""
        processed.add(item)
        for child in self.tree.get(item.id, []):
            self.add_descendants_to_processed(child, processed)
        return processed

    def iterate_menu(self, items, target_achieved=False, processed=None):
        """Iterates through a list of menu items, building the menu structure."""
        if processed is None:
            processed = set()

        result_dict = {}

        for item in items:
            if item in processed:
                continue

            if not target_achieved and item.url != self.item_url:
                children = self.tree.get(item.id, [])
                if not children:
                    result_dict[item] = {}
                    processed.add(item)
                else:
                    children_result, target_achieved, processed = self.iterate_menu(
                        children, target_achieved, processed)
                    result_dict[item] = children_result
                    processed.add(item)

            elif item.url == self.item_url:
                target_dict = {}
                for child in self.tree.get(item.id, []):
                    self.add_descendants_to_processed(child, processed)
                    target_dict[child] = {}
                self.add_descendants_to_processed(item, processed)
                result_dict[item] = target_dict
                target_achieved = True

            else:
                self.add_descendants_to_processed(item, processed)
                result_dict[item] = {}
                processed.add(item)

        return result_dict, target_achieved, processed

    def finalize_menu_dict(self, collection, level=0):
        """Generates html representation of the menu from a dictionary."""
        result_stack = []
        for element in collection:
            selected = ' class="selected"' if element.url == self.item_url else ''
            result_stack.append(
                '    ' * level + f'<li><a href="{self.query}{element.url}"{selected}>{element.name}</a></li>'
            )

            children = collection[element]
            if children:
                result_stack.append('    ' * (level + 1) + '<ul>')
                result_stack += self.finalize_menu_dict(children, level + 2)
                result_stack.append('    ' * (level + 1) + '</ul>')

        return result_stack

    def finalize_menu_flat(self, items):
        """Generates html representation of the folded menu (no item specified)."""
        return [
            f'<li><a href="{self.query}{item.url}">{item.name}</a></li>'
            for item in items
        ]

    def get_result(self):
        """Builds the final html representation of the menu."""
        root_items = self.tree.get(None, [])
        structure, found, _ = self.iterate_menu(root_items)

        if found:
            return self.finalize_menu_dict(structure)
        else:
            return self.finalize_menu_flat(root_items)
