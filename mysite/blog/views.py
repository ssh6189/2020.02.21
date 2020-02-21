from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import Form
from django.forms import CharField, Textarea, ValidationError
from django import forms
#from blog.forms import PostForm
from . import forms
from . import models

#기본적으로, get방식 가정
#아까는 신규작성이냐, 수정이냐
#이번에는 url 요청시 다음과 같은 형식을 지키도록 하게 바꿔보자
#<int.pk>/<mode>
'''
def list(request) :
    username = request.session["username"]
    user = User.objects.get(username=username)
    data = models.Post.objects.all().filter(author=user)
    context = {"data":data, "username":username}
    return render(request, "blog/list.html", context)

def detail(request, pk) :
    p = get_object_or_404(models.Post, pk=pk)
    return render(request, "blog/detail.html", {"d":p})
'''

class PostEditView(View) :
    def get(self, request, pk, mode):
        if mode == 'add':
            form = forms.PostForm()
        elif mode == 'list':
            username = request.session["username"]
            user = User.objects.get(username=username)
            data = models.Post.objects.all().filter(author=user)
            context = {"data":data, "username":username}
            return render(request, "blog/list.html", context)
        elif mode == 'detail':
            p = get_object_or_404(models.Post, pk=pk)
            return render(request, "blog/detail.html", {"d":p})
        elif mode == "edit":
            post = get_object_or_404(models.Post, pk=pk)
            form = forms.PostForm(instance=post)
        else:
            post = get_object_or_404(models.Post, pk=pk)
            form = forms.PostForm(instance=post)
        return render(request, "blog/edit.html", {"form":form})

    def post(self, request, pk, mode):

        username = request.session["username"]
        user = User.objects.get(username=username)

        if pk == 0:
            form = forms.PostForm(request.POST)
        else:
            post = get_object_or_404(models.Post, pk=pk)
            form = forms.PostForm(request.POST, instance=post)

#모듈화를 하면, 간단해지지만, 처음 보는 사람이 쓰기가 어렵다.
        if form.is_valid():
            #세이브를 하기 위해 세이브를 호출한것이 아니라, form객체로부터 model 데이터를 얻기 위해서이다.
            post = form.save(commit=False)
            if pk == 0:
                post.author = user
                post.save()
            else:
                post.publish()
            return redirect("list")
        return render(request, "blog/edit.html", {"form": form})


class LoginView(View) :
    def get(self, request):
        return render(request, "blog/login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user == None :
            return redirect("login")
        request.session["username"] = username
        return redirect("list")