"""# Models"""

from django.db.models import (
    CharField,
    PositiveSmallIntegerField,
    ForeignKey,
    SlugField,
    DateField,
    BooleanField,
    PROTECT,
)
from django.utils.translation import ugettext_lazy as _

from polymorphic.models import PolymorphicModel

from account.models import Account
from source.models import Source


class Transaction(PolymorphicModel):
    """
    ## Financial transaction

    This object if the main object of the project.
    """

    source = ForeignKey(
        verbose_name=_("source"),
        related_name="transaction_set",
        to=Source,
        blank=False,
        null=False,
        db_index=True,
        on_delete=PROTECT,
    )

    account = ForeignKey(
        verbose_name=_("account"),
        related_name="transaction_set",
        to=Account,
        blank=False,
        null=False,
        db_index=True,
        on_delete=PROTECT,
    )

    date = DateField(
        verbose_name=_("date"),
        blank=False,
        null=False,
        db_index=True,
    )

    name = CharField(
        verbose_name=_("name"),
        max_length=128,
        blank=False,
        null=False,
        db_index=True,
    )

    amount = PositiveSmallIntegerField(
        verbose_name=_("amount"),
        blank=False,
        null=False,
        db_index=True,
    )

    slug = SlugField(
        unique=True,
        max_length=32,
        editable=True,
        db_index=True,
    )

    def __str__(self):
        """Human readable representation"""
        return self.name

    def __repr__(self):
        """Technical representation"""
        return "<{} {}>".format(self._meta.object_name, self.name)

    class Meta:  # pylint: disable=too-few-public-methods
        """Transaction Meta class"""

        verbose_name = _("transaction")
        verbose_name_plural = _("transactions")
        ordering = ("-date", "name")
        index_together = (
            ("source", "name"),
            ("account", "name"),
            ("source", "account"),
            ("source", "account", "name"),
        )


class Expense(Transaction):
    """
    ## Expense model

    This object represents a transaction that is an actual expense.
    """

    class Meta(Transaction.Meta):  # pylint: disable=too-few-public-methods
        """Expense Meta class"""

        verbose_name = _("expense")
        verbose_name_plural = _("expenses")


class Foresight(Transaction):
    """
    ## Foresight model

    This model represent a transaction that is an anticipation of a planned and recurrent expense.
    """

    FREQUENCY = (
        ("d", _("daily")),
        ("w", _("weekly")),
        ("m", _("monthly")),
        ("y", _("yearly")),
    )

    frequency = CharField(
        verbose_name=_("frequency"),
        max_length=1,
        blank=False,
        null=False,
        db_index=True,
        choices=FREQUENCY,
    )

    active = BooleanField(
        verbose_name=_("active"),
        db_index=True,
    )

    class Meta(Transaction.Meta):  # pylint: disable=too-few-public-methods
        """Foresight Meta class"""

        verbose_name = _("foresight")
        verbose_name_plural = _("foresights")
