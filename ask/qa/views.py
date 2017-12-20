# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_GET

from qa.models import Question
from qa.forms import AskForm, AnswerForm


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


def login(request):
    return HttpResponse("Here you can login")


def signup(request):
    return HttpResponse("Here you can Sign up")


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
