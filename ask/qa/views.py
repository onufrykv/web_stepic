# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse 


def home(request):
    return HttpResponse("Home page")


def login(request):
    return HttpResponse("Here you can login")


def signup(request):
    return HttpResponse("Here you can Sign up")


def question(request, num_question):
    return HttpResponse("Question number: {}".format(num_question))


def ask(request):
    return HttpResponse("Ask me something")


def popular(request):
    return HttpResponse("Here will be popular questions")


def new(request):
    return HttpResponse("Here will be new questions")
