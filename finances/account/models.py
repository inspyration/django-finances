"""# Models"""

from django.db.models import (
    Model,
    CharField,
    PositiveSmallIntegerField,
    ForeignKey,
    SlugField,
    PROTECT,
)
from django.utils.translation import ugettext_lazy as _

from bank.models import Bank


class Account(Model):
    """
    ## Bank Account

    A significant level of aggregation.
    """

    bank = ForeignKey(
        verbose_name=_("bank"),
        related_name="account_set",
        to=Bank,
        blank=False,
        db_index=True,
        on_delete=PROTECT,
    )

    name = CharField(
        verbose_name=_("name"),
        max_length=32,
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

    amount = PositiveSmallIntegerField(
        verbose_name=_("Amount"),
        blank=False,
        null=False,
        default=0,
    )

    def __str__(self):
        """Human readable representation"""
        return self.name

    def __repr__(self):
        """Technical representation"""
        return "<{} {}>".format(self._meta.object_name, self.name)

    class Meta:  # pylint: disable=too-few-public-methods
        """Bank account Meta class"""

        verbose_name = _("account")
        verbose_name_plural = _("accounts")
        ordering = ("name",)
        index_together = (("bank", "name"),)
        unique_together = (("bank", "name"),)
