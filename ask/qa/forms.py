from django import forms
from qa.models import Question, Answer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)

    def clean(self):
        pass

    def save(self):
        question = Question(**self.cleaned_data)
        question.author_id = self._user.id
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput)

    def clean_question(self):
        id_qw = self.cleaned_data['question']
        try:
            question = Question.objects.get(id=id_qw)
        except Question.DoesNotExist:
            raise forms.ValidationError('There is not question with id = {}'.format(id_qw))
        return question

    def clean(self):
        pass

    def save(self):
        self.cleaned_data['author'] = self._user
        answer = Answer(**self.cleaned_data)
        answer.save()
        return answer


class SignupForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
            raise forms.ValidationError('User with such login already exists')
        except User.DoesNotExist:
            pass
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password = make_password(password)
        return password

    def clean(self):
        pass

    def save(self):
        user = User(**self.cleaned_data)
        user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        message = 'Wrong Username or password'
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(message)
        if not user.check_password(password):
            raise forms.ValidationError(message)
