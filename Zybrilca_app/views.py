from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import *
from .forms import *
from django.db.models import Q


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
        edit_word_pair_form = WordPairForm()
        new_wordpair = WordPair()
        new_wordpair_form = WordPairForm(request.POST)
        list_pairs_forms = list()
        list_pairs_forms.append(new_wordpair_form)
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
            'list_pairs_forms': list_pairs_forms,
        }

    return render(request, 'ilya_test_forms.html', context)


@csrf_exempt
def dictionary_testing(request, dict_id):
    if request.user.is_authenticated:
        dictionary = Dictionary.objects.get(pk=dict_id)
        wordpairs_list = dictionary.wordpair_set.all()
        count = wordpairs_list.count()
        answer = ''
        if request.method == "GET":
            request.session["wordIndex"] = 0
            request.session["result"] = 0
        if request.method == "POST":
            word1 = wordpairs_list[request.session["wordIndex"]].word_translation
            word2 = request.POST.get('userWord')
            if word1 == word2:
                request.session["result"] += 1
                answer = "Правильно"
            else:
                answer = "Неправильно"
            if request.session["wordIndex"] != count:
                request.session["wordIndex"] += 1
        if request.session["wordIndex"] != count:
            testWord = wordpairs_list[request.session["wordIndex"]]
        else:
            testWord = ''
        if request.session["wordIndex"] == 0:
            prevWord = ''
        else:
            prevWord = wordpairs_list[request.session["wordIndex"] - 1]
        context = {
            'dictionary': dictionary,
            'wordpairs_list': wordpairs_list,
            'result': request.session["result"],
            'count': count,
            'testWord' : testWord,
            'prevWord' : prevWord,
            'wordIndex' : request.session["wordIndex"],
            'answer' : answer,
            'userWord' : request.POST.get('userWord')
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
