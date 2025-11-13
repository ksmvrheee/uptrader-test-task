from django.contrib import admin
from .models import MainMenuItem, SecondaryMenuItem


class MenuAdmin(admin.ModelAdmin):
    """Baseclass to customize menu models' in the admin panel."""
    prepopulated_fields = {'url': ('name',)}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'parent':
            kwargs['queryset'] = self.model.objects.order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(MainMenuItem)
class MainMenuItemAdmin(MenuAdmin):
    pass


@admin.register(SecondaryMenuItem)
class SecondaryMenuItemAdmin(MenuAdmin):
    pass
