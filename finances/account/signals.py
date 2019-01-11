"""App signals module"""

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from account.models import Account


#
# Receivers
#


@receiver(pre_save, sender=Account, dispatch_uid="account_pre_created")
def account_pre_created(sender, instance, raw, using, update_fields, **kwargs):  # pylint: disable=unused-argument
    """Create lug"""
    if instance.pk:  # Called only on creation
        return

    # from nose.tools import set_trace; set_trace()

    if not instance.slug:
        instance.slug = slugify(instance.bank.name + "__" + instance.name)
