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

    def __str__(self):
        return self.dict_name


class WordPair(models.Model):
    word = models.CharField('Переводимое слово', max_length=40)
    word_translation = models.CharField('Перевод', max_length=40)
    dictionary_parent = models.ForeignKey(Dictionary, on_delete=models.CASCADE)

    def __str__(self):
        return str("{} (PARENT) - {}".format(self.dictionary_parent, self.word))


class MarkForAnswer(models.Model):
    mark_value = models.FloatField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE)


class BookMark(models.Model):
    added_dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE)
    user_added = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('added_dictionary', 'user_added')
