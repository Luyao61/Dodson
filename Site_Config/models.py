from django.db import models


# Create your models here.
class SingletonModel(models.Model):
    """Singleton Django Model
    Ensures there's always only one entry in the database, and can fix the
    table (by deleting extra entries) even if added via another mechanism.
    Also has a static load() method which always returns the object - from
    the database if possible, or a new empty (default) instance if the
    database is still empty. If your instance has sane defaults (recommended),
    you can use it immediately without worrying if it was saved to the
    database or not.
    Useful for things like system-wide user-editable settings.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Save object to the database. Removes all other entries if there
        are any.
        """
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        bypass the delete method on the admin site;
        This object can only be modified; but not deleted
        """
        pass

    @classmethod
    def load(cls):
        """
        Load object from the database. Failing that, create a new empty
        (default) instance of the object and return it (without saving it
        to the database).
        """

        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


class SiteSetting(SingletonModel):
    EX_CONFIDENCE_SCORE = ( (0, 0), (20, 20), (40, 40), (60, 60), (80, 80), (100, 100), )
    response_limit = models.PositiveSmallIntegerField(default=80)
    manipulation_check_threshold = models.PositiveSmallIntegerField(
        choices=EX_CONFIDENCE_SCORE,
        default=60
    )

    def threshold(self):
        return self.manipulation_check_threshold
    threshold.short_description = 'Exclude sample responses smaller or equal to:'
