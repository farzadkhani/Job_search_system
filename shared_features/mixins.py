from django.contrib import admin
from django.db import models


class SoftDeleteMixinQuerySet(models.QuerySet):
    """
    Custom queryset for models using SoftDeleteMixin, providing methods 
    for soft deletion and permanent deletion.
    """
    def delete(self):
        """Soft deletes the records in the current queryset."""
        return self.update(is_removed=True)

    def purge(self):
        """Permanently deletes the records in the current queryset."""
        return super().delete()


class SoftDeleteMixinManager(models.Manager):
    """
    Custom manager for models using SoftDeleteMixin, providing methods to 
    retrieve active, deleted, and all records.
    """
    def get_queryset(self):
        """Returns a queryset of active (not soft-deleted) records."""
        return SoftDeleteMixinQuerySet(self.model, using=self._db).exclude(
            is_removed=True
        )

    def deleted(self):
        """Returns a queryset of soft-deleted records."""
        return SoftDeleteMixinQuerySet(self.model, using=self._db).filter(
            is_removed=True
        )

    def active(self):
        """Alias for get_queryset(), returns a queryset of active records."""
        return self.get_queryset().filter(is_removed=False)

    def deactivate(self):
        """Alias for deleted(), returns a queryset of soft-deleted records."""
        return self.get_queryset().filter(is_removed=True)

    def everything(self):
        """Returns a queryset of all records, including soft-deleted ones."""
        return SoftDeleteMixinQuerySet(self.model, using=self._db)


class TimeStampMixin(models.Model):
    """
    Abstract model mixin that automatically adds 'created_at' and 
    'updated_at' timestamp fields to the model.
    """
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SoftDeleteMixin(models.Model):
    """
    Abstract model mixin that implements soft deletion functionality. 
    Instead of permanently deleting records, it sets the 'is_removed' 
    field to True.
    """
    class Meta:
        abstract = True

    is_removed = models.BooleanField(default=False)
    objects = SoftDeleteMixinManager()

    def delete(self, *args, **kwargs):
        """Overrides the default delete method to perform soft deletion."""
        self.is_removed = True

        self.save()

    def purge(self, using=None, keep_parents=False):
        """
        Optional method for permanently deleting the record. 
        Use with caution.
        """
        return super().delete(using=using, keep_parents=keep_parents)


class ModelMixin(TimeStampMixin, SoftDeleteMixin):
    """
    Abstract model mixin that combines TimeStampMixin and SoftDeleteMixin 
    for models that require both timestamping and soft deletion.
    """
    class Meta:
        abstract = True


class ModelAdminMixin(admin.ModelAdmin):
    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        qs = self.model._default_manager.everything()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs