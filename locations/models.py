from django.db import models


class City(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Cities'
        db_table = "locations_city"

    def __str__(self):
        return '%s (id:%s)' % (self.name, self.id)
