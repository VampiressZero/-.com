from django.db import models

# Create your models here.

class Dictionary(models.Model):
    dict_name = models.CharField('Название словаря', max_length=40)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    description = models.TextField('Краткое описание словаря')
    user_created = models.ForeignKey()