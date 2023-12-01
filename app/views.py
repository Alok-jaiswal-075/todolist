from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate , login as loginUser , logout
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from app.forms import TODOForm
from app.models import TODO
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        todos = TODO.objects.filter(user = user)
        # return render(request , 'index.html' , context={'form' : form , 'todos' : todos})
        return HttpResponse("this is home page", content_type="application/text")


def login(request):
    if request.method == 'GET':
        form1 = AuthenticationForm()
        context = {
            "form" : form1
        }
        return render(request , 'login.html' , context=context )
    else:
        form = AuthenticationForm(data=request.POST)
        print(request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username , password = password)
            if user is not None:
                loginUser(request , user)
                # return redirect('home')
                return HttpResponse("logged in successfully", content_type="application/text")
        else:
            context = {
                "form" : form
            }
            # return render(request , 'login.html' , context=context )
            return HttpResponse("login failed", content_type="application/text")


def signup(request):

    if request.method == 'GET':
        form = UserCreationForm()
        context = {
            "form" : form
        }
        return render(request , 'signup.html' , context=context)
    else:
        print(request.POST)
        form = UserCreationForm(request.POST)  
        print(request.POST)
        context = {
            "form" : form
        }
        try:
            form.is_valid()
            user = form.save()
            print(user)
            if user is not None:
                # return redirect('login')
                return HttpResponse("User added successfully", content_type="application/text")
        except Exception as e:
            print(form.errors)
            print(e)
            # return render(request , 'signup.html' , context=context)
            return HttpResponse("signup failed", content_type="application/text")



@login_required(login_url='login')
def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        form = TODOForm(request.POST)
        # print(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            print(todo.id)
            if request.user.is_authenticated:
                user = request.user
                form = TODOForm()
                todos = TODO.objects.filter(user = user)
                print(todos)
            return HttpResponse(todos, content_type="application/json")
            # return redirect("home")
        else: 
            return HttpResponse("cannot add todo", content_type="application/text")
            # return render(request , 'index.html' , context={'form' : form})



def delete_todo(request , id ):
    print(id)
    TODO.objects.get(pk = id).delete()
    return HttpResponse("deleted todo", content_type="application/text")
    # return redirect('home')


def change_todo(request , id  , status):
    todo = TODO.objects.get(pk = id)
    todo.status = status
    todo.save()
    return HttpResponse("changed todo status", content_type="application/text")
    # return redirect('home')

def signout(request):
    logout(request)
    return HttpResponse("logged out successfully", content_type="application/text")
    # return redirect('login')