from django.db.models import Model, BooleanField


class ActiveMixin(Model):
    is_active = BooleanField(default=True)

    class Meta:
        abstract = True

    def delete(self, forced_delete=False, *args, **kwargs):
        if not forced_delete:
            self.is_active = False
            self.save()
        else:
            super().delete(*args, **kwargs)

