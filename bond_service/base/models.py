from django.db.models import Model, DateTimeField
from django.utils import timezone


class BaseModel(Model):
    created_at = DateTimeField(default=timezone.now, editable=False)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)
