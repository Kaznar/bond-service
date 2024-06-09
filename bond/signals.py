from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from bond_service.base.cache_keys import investment_analysis_cache_key
from .models import Bond


@receiver(post_save, sender=Bond)
@receiver(post_delete, sender=Bond)
def invalidate_cache(sender, instance, **kwargs):
    cache_key = investment_analysis_cache_key(instance.user.id)
    cache.delete(cache_key)
