from django import forms
from .models import *


class DictionaryForm(forms.ModelForm):
    class Meta:
        model = Dictionary
        fields = ('dict_name', 'description',)


class WordPairForm(forms.ModelForm):
    class Meta:
        model = WordPair
        fields = ('word', 'word_translation',)