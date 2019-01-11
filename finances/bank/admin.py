"""# Admin IHM"""


from django.contrib.admin import ModelAdmin
from django.contrib.admin.decorators import register

from bank.models import Bank


@register(Bank)
class BankAdmin(ModelAdmin):
    """
    ## Bank admin IHM

    This object cannot be modified after being created.
    So we can only create or view this object.
    They only can be created from the Account Form
    There are any specific IHM to manage banks
    """

    model = Bank
    fields = ("name", "slug")
    readonly_fields = ("slug",)
    list_display = ("name",)
    search_fields = ("name",)

    def has_module_permission(self, request):
        """Cannot be accessed from home page"""
        return False

    def has_add_permission(self, request):
        """Can add an object"""
        return True

    def has_delete_permission(self, request, obj=None):
        """Cannot delete an object"""
        return False

    def has_change_permission(self, request, obj=None):
        """Cannot change an object"""
        return False

    def has_view_permission(self, request, obj=None):
        """Can view an object"""
        return True
