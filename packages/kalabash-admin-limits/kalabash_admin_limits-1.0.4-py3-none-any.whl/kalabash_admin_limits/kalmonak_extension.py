# coding: utf-8

"""
The *limits* extension
----------------------
"""
from django.utils.translation import ugettext_lazy

from kalabash.core.extensions import KalmonakExtension, exts_pool
from kalabash.core.models import User
from kalabash.lib import events, parameters

from .models import LimitTemplates, LimitsPool, Limit


EVENTS = [
    'GetExtraLimitTemplates'
]


class Limits(KalmonakExtension):
    name = "kalabash_admin_limits"
    label = "Limits"
    version = "1.0.2"
    description = ugettext_lazy(
        "Per administrator resources to limit the number of objects "
        "they can create"
    )
    url = "limits"

    def load(self):
        from .app_settings import ParametersForm
        from . import controls

        parameters.register(ParametersForm, ugettext_lazy("Limits"))
        events.declare(EVENTS)
        from . import general_callbacks

    def load_initial_data(self):
        """Create pools for existing accounts."""
        for user in User.objects.filter(groups__name="DomainAdmins"):
            pool, created = LimitsPool.objects.get_or_create(user=user)
            for tpl in LimitTemplates().templates:
                Limit.objects.get_or_create(name=tpl[0], pool=pool, maxvalue=0)

exts_pool.register_extension(Limits)
