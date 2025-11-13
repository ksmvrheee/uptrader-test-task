from django.db import models


class MainMenuItem(models.Model):
    """Represents an item of the main menu."""
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True,
                               on_delete=models.CASCADE, related_name='children')

    menu_label = 'main_menu'  # label to distinguish

    class Meta:
        unique_together = ('parent', 'name')

    def __str__(self):
        return self.name


class SecondaryMenuItem(models.Model):
    """Represents an item of the secondary menu."""
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True,
                               on_delete=models.CASCADE, related_name='children')

    menu_label = 'secondary_menu'  # label to distinguish

    class Meta:
        unique_together = ('parent', 'name')

    def __str__(self):
        return self.name
