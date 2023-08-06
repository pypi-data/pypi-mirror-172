from django.conf import settings
from django.db.models import options
from django.db.models.signals import class_prepared, pre_init

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('db_prefix',)


def model_prefix(sender, **kwargs):
    # Global defined prefix
    prefix = getattr(settings, "DB_PREFIX", None)

    # Model defined prefix
    if hasattr(sender._meta, 'db_prefix'):
        prefix = sender._meta.db_prefix

    if prefix and not sender._meta.db_table.startswith(prefix):
        sender._meta.db_table = prefix + sender._meta.db_table


pre_init.connect(model_prefix)
class_prepared.connect(model_prefix)
