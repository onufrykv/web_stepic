# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_GET
from django.contrib.auth import authenticate, login

from qa.models import Question
from qa.forms import AskForm, AnswerForm, SignupForm, LoginForm


@require_GET
def home(request):
    questions = Question.objects.new()
    page = request.GET.get('page', 1)
    paginator = Paginator(questions, 10)
    paginator.baseurl = '/?page='

    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render(request, 'news.html', {
        'questions': page.object_list,
        'paginator': paginator, 'page': page,
    })


def login_u(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            usname = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=usname, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form,
                                          'user': request.user,
                                          'session': request.session,
                                           })


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            usname = form.cleaned_data["username"]
            user = authenticate(username=usname, password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = SignupForm()
    return render(request, 'singup.html', {'form': form,
                                           'user': request.user,
                                           'session': request.session,
                                           })


def question(request, num_question):
    quest = get_object_or_404(Question, id=num_question)

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            form._user = request.user
            form.save()
            url = quest.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm(initial={'question': quest.id})

    return render(request, 'question.html', {'question': quest,
                                             'form': form,
                                             })


def ask(request):
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
            form._user = request.user
            quest = form.save()
            url = quest.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, "ask.html", {"form": form,
                                        "user": request.user,
                                        })


@require_GET
def popular(request):
    questions = Question.objects.popular()
    page = request.GET.get('page', 1)
    paginator = Paginator(questions, 10)
    paginator.baseurl = '/popular/?page='

    try:
        page = paginator.page(page)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render(request, 'news.html', {
        'questions': page.object_list,
        'paginator': paginator, 'page': page,
    })


def new(request):
    return HttpResponse("Here will be new questions")
