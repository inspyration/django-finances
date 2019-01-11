"""# Admin IHM"""


from datetime import date

from django.contrib.admin import HORIZONTAL, SimpleListFilter
from django.contrib.admin.decorators import register
from django.contrib.admin.views.main import ChangeList
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicParentModelAdmin, PolymorphicChildModelFilter

from transaction.models import Transaction, Expense, Foresight


class TransactionMonthListFilter(SimpleListFilter):
    """
    ## Month filter for Transaction list IHM

    This objects allow to filter transactions according to any month effectively used in at least one transaction.
    This is a transaction specific filter.
    """

    # Human-readable title which will be displayed in the right admin sidebar just above the filter options.
    title = _('month')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'month'

    def lookups(self, request, model_admin):
        """Generator that get used months and format it"""
        for month in model_admin.get_queryset(request).dates("date", "month", order="DESC"):
            yield (month.strftime("%m-%Y"), month.strftime("%B %Y"))

    def queryset(self, request, queryset):
        """Query set to get actually used months"""
        value = self.value()
        if value is None:
            return queryset

        try:
            start_month, start_year = map(int, value.split("-"))
        except ValueError:
            return queryset

        if start_month == 12:
            end_month, end_year = 1, start_year + 1
        else:
            end_month, end_year = start_month + 1, start_year

        return queryset.filter(date__gte=date(start_year, start_month, 1), date__lt=date(end_year, end_month, 1))


class TransactionChangeList(ChangeList):
    """
    ## Transaction specific change list

    The purpose of this customization is to add a sum to the amount column (this sum varies along with filters).
    """

    def get_results(self, request):
        """Overridden method to add the specific feature adding the sum on the amount column"""
        super().get_results(request)
        qs = self.result_list.aggregate(sum=Sum('amount'))
        self.sum = qs['sum']


class TransactionChildAdmin(PolymorphicChildModelAdmin):
    """
    ## Transaction base admin IHM

    This object if the main object of the project.
    This object can be created / updated / deleted.
    This IHM can be used as is and with the polymorphic child objects. Those would work the same way.
    """

    @staticmethod
    def source_category(obj):
        """Shortcut to the category of the source, for list view"""
        return obj.source.category
    source_category.short_description = _("Category")

    base_model = Transaction
    # fields = ("source", "account", "date", "name", "amount", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("source__name", "account__name", "date", "name")
    autocomplete_fields = ("source", "account")
    list_filter = ("source__category", TransactionMonthListFilter, "source", "account")
    # list_display = ("polymorphic_ctype", "source", "account", "date", "name", "amount")
    list_display = ("polymorphic_ctype", "source_category", "source", "account", "date", "name", "amount")

    def get_changelist(self, request, **kwargs):
        """Add the transaction specific change list that add the sum on the amount column"""
        return TransactionChangeList

    def has_module_permission(self, request):
        """Can be accessed from home page"""
        return True

    def has_add_permission(self, request):
        """Can add an object"""
        return True

    def has_delete_permission(self, request, obj=None):
        """Can delete an object"""
        return True

    def has_change_permission(self, request, obj=None):
        """Can update an object"""
        return True

    def has_view_permission(self, request, obj=None):
        """Can view an object"""
        return True


@register(Expense)
class ExpenseAdmin(TransactionChildAdmin):
    """
    ## Expense specific admin IHM

    This object represents a transaction that is an actual expense.
    """

    base_model = Expense
    show_in_index = True
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("source", "date", "name"),
                    ("account", "amount"),
                )
            }),
        (_("Technical information"), {
            "fields": (
                ("slug",),
            )
        }),
    )


@register(Foresight)
class ForesightAdmin(TransactionChildAdmin):
    """
    ## Expense specific admin IHM

    This object represents a transaction that is an anticipation of a planned and recurrent expense.
    """

    base_model = Foresight
    show_in_index = True
    radio_fields = {"frequency": HORIZONTAL}
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("source", "date", "name"),
                    ("account", "amount"),
                )
            }),
        (_("Settings"), {
            "fields": (
                ("active", "frequency"),
            )
        }),
        (_("Technical information"), {
            "fields": (
                ("slug",),
            )
        }),
    )


@register(Transaction)
class ContactParentAdmin(PolymorphicParentModelAdmin):
    """
    ## Actual IHM for transactions and theirs polymorphic children

    Some features need to be repeated here to work for the transaction object itself
    (childs objects use Child model admin).
    """

    def get_changelist(self, request, **kwargs):
        """Add the transaction specific change list that add the sum on the amount column"""
        return TransactionChangeList

    @staticmethod
    def source_category(obj):
        """Shortcut to the category of the source, for list view"""
        return obj.source.category
    source_category.short_description = _("Category")

    base_model = Transaction
    child_models = (Expense, Foresight)
    list_filter = (PolymorphicChildModelFilter, "source__category", TransactionMonthListFilter, "source", "account")
    list_display = ("polymorphic_ctype", "source_category", "source", "account", "date", "name", "amount")
