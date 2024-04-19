from django.db import models


# Create your models here.
class Case(models.Model):
    objects = None
    name: models.CharField('Название дела', max_length=255)

    class Meta:
        db_table = 'case'
