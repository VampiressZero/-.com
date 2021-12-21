from io import StringIO

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from .models import *
from .forms import *
from django.db.models import Q
from wsgiref.util import FileWrapper



# Create your views here.
def index(request):
    return render(request, 'index.html')


@csrf_exempt
def reg(request):
    if request.method == "POST":
        username = request.POST.get('login', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        passwordConfirm = request.POST.get('passwordConfirm', None)
        if password != passwordConfirm:
            error = "Пароли не совпадают"
            return render(request, 'reg.html', locals())
        users = User.objects.all()
        for i in users:
            if i.username == username:
                error = "Пользователь с таким логином уже существует"
                return render(request, 'reg.html', locals())
            if i.email == email:
                error = "Пользователь с такой почтой уже существует"
                return render(request, 'reg.html', locals())
        user = User.objects.create_user(username=username, password=password, email=email)
        return render(request, 'reg.html', locals())
    return render(request, 'reg.html', locals())


@csrf_exempt
def login_(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    username = request.POST.get('login', None)
    password = request.POST.get('password', None)
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            error = "Учетная запись не активирована"
            return render(request, 'index.html', locals())
    else:
        error = "Неверный логин или пароль"
        return render(request, 'index.html', locals())


@csrf_exempt
def logout_(request):
    logout(request)
    return HttpResponseRedirect('/')


@csrf_exempt
def show_dictionaries(request):
    list_dictionaries = Dictionary.objects.all()
    return HttpResponse(list_dictionaries[0].text_pairs)


@csrf_exempt
def temp_show_lists(request):
    return render(request, 'Cards.html')


@csrf_exempt
def create_dictionary(request):
    if request.user.is_authenticated:
        new_dictionary_form = DictionaryForm(request.POST)
        new_dictionary = Dictionary()
        new_wordpair = WordPair()
        new_wordpair_form = WordPairForm(request.POST)
        if request.method == 'POST':
            if new_dictionary_form.is_valid() & new_wordpair_form.is_valid():
                new_dictionary.dict_name = new_dictionary_form.cleaned_data.get('dict_name')
                new_dictionary.description = new_dictionary_form.cleaned_data.get('description')
                new_dictionary.user_created = request.user
                new_wordpair.word = new_wordpair_form.cleaned_data.get('word')
                new_wordpair.word_translation = new_wordpair_form.cleaned_data.get('word_translation')
                new_wordpair.dictionary_parent = new_dictionary
                new_dictionary.save()
                new_wordpair.save()
                return redirect('Zybrilca_app:profile')
            else:
                return HttpResponse("Форма Недействительна!")
        context = {
            'new_dictionary_form': new_dictionary_form,
            'new_wordpair_form': new_wordpair_form,
        }

    return render(request, 'create_dictionary.html', context)


@csrf_exempt
def dictionary_testing(request, dict_id):
    if request.user.is_authenticated:
        dictionary = Dictionary.objects.get(pk=dict_id)
        wordpairs_list = dictionary.wordpair_set.all()
        count = wordpairs_list.count()
        answer = ''
        testList = []
        if request.method == "GET":
            request.session["wordIndex"] = 0
            request.session["result"] = 0
            request.session["testIds"] = []
        if request.method == "POST":
            word1 = wordpairs_list[request.session["wordIndex"]].word_translation
            word2 = request.POST.get('userWord')
            if word1.lower() == word2.lower():
                request.session["result"] += 1
                answer = "Правильно"
            else:
                answer = "Неправильно"
            if request.session["wordIndex"] != count:
                request.session["wordIndex"] += 1
        if request.session["wordIndex"] != count:
            testWord = wordpairs_list[request.session["wordIndex"]]
            request.session["testIds"].append(testWord.id)
        else:
            testWord = ''
            for w in request.session["testIds"]:
                testList.append(WordPair.objects.get(pk=w))
        if request.session["wordIndex"] == 0:
            prevWord = ''
        else:
            prevWord = wordpairs_list[request.session["wordIndex"] - 1]

        context = {
            'dictionary': dictionary,
            'wordpairs_list': wordpairs_list,
            'result': request.session["result"],
            'count': count,
            'testWord': testWord,
            'prevWord': prevWord,
            'wordIndex': request.session["wordIndex"],
            'answer': answer,
            'userWord': request.POST.get('userWord'),
            'testList': testList
        }
        return render(request, 'Cards.html', context)


@csrf_exempt
def profile(request):
    if request.user.is_authenticated:
        list_dictionaries = request.user.dictionary_set.all()
        list_dictionaries_self = Dictionary.objects.filter(Q(is_removed=False) & Q(user_created=request.user))
        word = Dictionary()
        context = {
            'list_dictionaries': list_dictionaries,
            'list_dictionaries_self': list_dictionaries_self,
        }
        return render(request, 'Profile.html', context)


@csrf_exempt
def edit_dictionary(request, dict_id, word_id = ''):
    dictionary = Dictionary.objects.get(pk=dict_id)
    wordList = dictionary.wordpair_set.all()
    currentWord = WordPair()
    if word_id != '':
        currentWord = WordPair.objects.get(pk=word_id)
    context = {
        'dictionary': dictionary,
        'wordList': wordList,
        'currentWord' : currentWord
    }
    return render(request, 'Lists_main.html', context)


@csrf_exempt
def remove_dictionary(request):
    if request.method == 'POST':
        choices = request.POST.getlist('choice')
        for choice in choices:
            remove_dict = Dictionary.objects.get(pk=choice)
            remove_dict.is_removed = True
            remove_dict.save()
    return redirect('Zybrilca_app:profile')


@csrf_exempt
def edit_word(request, dict_id, wordpair_id):
    return HttpResponse("sas")


@csrf_exempt
def add_word(request, dict_id):
    if request.user.is_authenticated:
        dictionary = Dictionary.objects.get(pk=dict_id)
        new_wordpair_form = WordPairForm(request.POST)
        new_wordpair = WordPair()
        if request.method == 'POST':
            if new_wordpair_form.is_valid():
                new_wordpair.word = new_wordpair_form.cleaned_data.get('word')
                new_wordpair.word_translation = new_wordpair_form.cleaned_data.get('word_translation')
                new_wordpair.dictionary_parent = dictionary
                new_wordpair.save()
                return redirect('Zybrilca_app:edit_dictionary', dictionary.id)
            else:
                return HttpResponse("Форма Недействительна!")

        context = {
            'new_wordpair_form': new_wordpair_form,
            'dictionary': dictionary
        }
        return render(request, 'add_word.html', context)
    else:
        return HttpResponse('Зарегистрируйся, дружок-пирожок!')


@csrf_exempt
def remove_wordpair(request, dict_id, wordpair_id):
    dictionary = Dictionary.objects.get(pk=dict_id)
    if request.user.is_authenticated:
        if request.method == 'POST':
            word_on_remove = WordPair.objects.get(pk=wordpair_id)
            word_on_remove.delete()
            return redirect('Zybrilca_app:edit_dictionary', dictionary.id)
    else:
        return HttpResponse('А авторизироваться кто будет?')


def refactor_dict_to_txt(dictionary):
    edited_wordpairs = ""
    list_wordpairs = dictionary.wordpair_set.all()
    for wordpair in list_wordpairs:
        edited_wordpairs += wordpair.word + ", " + wordpair.word_translation + "\n"
    return edited_wordpairs

def download_dictionary(request, dict_id):
    dict_on_download = Dictionary.objects.get(pk=dict_id)
    file = refactor_dict_to_txt(dict_on_download)
    return HttpResponse(open('dict.txt', 'w+'))


