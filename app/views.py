from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as loginUser, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from app.forms import TODOForm
from app.models import TODO
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        # Unused variables removed: form and todos
        return HttpResponse("This is the home page", content_type="application/text")


def login(request):
    if request.method == 'GET':
        form1 = AuthenticationForm()
        context = {
            "form": form1
        }
        return render(request, 'login.html', context=context)
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                loginUser(request, user)
                return HttpResponse("Logged in successfully", content_type="application/text")
        else:
            context = {
                "form": form
            }
            return HttpResponse("Login failed", content_type="application/text")


def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        context = {
            "form": form
        }
        return render(request, 'signup.html', context=context)
    else:
        form = UserCreationForm(request.POST)
        context = {
            "form": form
        }
        try:
            form.is_valid()
            user = form.save()
            if user is not None:
                return HttpResponse("User added successfully", content_type="application/text")
        except Exception as e:
            print(e)
            return HttpResponse("Signup failed", content_type="application/text")


@login_required(login_url='login')
def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            return HttpResponse("Todo added successfully", content_type="application/text")
        else:
            return HttpResponse("Cannot add todo", content_type="application/text")


def delete_todo(request, id):
    TODO.objects.get(pk=id).delete()
    return HttpResponse("Deleted todo", content_type="application/text")


def change_todo(request, id, status):
    todo = TODO.objects.get(pk=id)
    todo.status = status
    todo.save()
    return HttpResponse("Changed todo status", content_type="application/text")


def signout(request):
    logout(request)
    return HttpResponse("Logged out successfully", content_type="application/text")
