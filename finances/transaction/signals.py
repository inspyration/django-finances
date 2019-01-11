"""App signals module"""
from uuid import uuid4

from django.db.models.signals import pre_save
from django.dispatch import receiver

from transaction.models import Transaction, Expense, DirectDebit


#
# Receivers
#


@receiver(pre_save, sender=Transaction, dispatch_uid="transaction_pre_created")
@receiver(pre_save, sender=Expense, dispatch_uid="expense_pre_created")
@receiver(pre_save, sender=DirectDebit, dispatch_uid="direct_debit_pre_created")
def transaction_pre_created(sender, instance, raw, using, update_fields, **kwargs):  # pylint: disable=unused-argument
    """Create name and slug"""
    if instance.pk:  # Called only on creation
        return

    # from nose.tools import set_trace; set_trace()

    if not instance.slug:
        instance.slug = uuid4()
