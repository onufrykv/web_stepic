# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_GET

from qa.models import Question


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
    question = get_object_or_404(Question, id=num_question)
    return render(request, 'question.html', {
        'question': question,
    })


def ask(request):
    return HttpResponse("Ask me something")


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
