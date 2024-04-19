from django.db import models


# Create your models here.
class CommonMailingList(models.Model):
    objects = None
    email = models.EmailField('Email подписчика')

    class Meta:
        db_table = 'common_mailing_list'


class CaseMailingList(models.Model):
    email = models.EmailField('Email подписчика')
    case = models.ForeignKey(to='cases.Case', verbose_name='Дело', on_delete=models.CASCADE)

    class Meta:
        db_table = 'case_mailing_list'
