from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.


# class User(AbstractUser):


class Dictionary(models.Model):
    dict_name = models.CharField('Название словаря', max_length=40)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    description = models.TextField('Краткое описание словаря')
    user_created = models.ForeignKey(User, on_delete=models.CASCADE)
    text_pairs = models.TextField('Необработанные пары слов')
