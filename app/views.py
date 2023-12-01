from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login as loginUser, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from app.forms import TODOForm
from app.models import TODO
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
import json


@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        # Unused variables removed: form and todos
        return HttpResponse("This is the home page", content_type="text/html")


def login(request):
    if request.method == 'GET':
        return HttpResponse("This is login form", content_type="text/html")
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                loginUser(request, user)
                return HttpResponse("Logged in successfully", content_type="text/html")
        else:
            return HttpResponse("Login failed", content_type="text/html")


def signup(request):
    if request.method == 'GET':
        return HttpResponse("This is signup form", content_type="text/html")
    else:
        form = UserCreationForm(request.POST)
        try:
            form.is_valid()
            user = form.save()
            if user is not None:
                return HttpResponse("User added successfully", content_type="text/html")
        except Exception as e:
            print(e)
            return HttpResponse("Signup failed", content_type="text/html")


@login_required(login_url='login')
def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            return HttpResponse("Todo added successfully", content_type="text/html")
        else:
            return HttpResponse("Cannot add todo", content_type="text/html")


def delete_todo(request, id):
    TODO.objects.get(pk=id).delete()
    return HttpResponse("Deleted todo", content_type="text/html")


def change_todo(request, id, status):
    todo = TODO.objects.get(pk=id)
    todo.status = status
    todo.save()
    return HttpResponse("Changed todo status", content_type="text/html")


def signout(request):
    logout(request)
    return HttpResponse("Logged out successfully", content_type="text/html")


def all_tasks(request):
    if request.user.is_authenticated:
        tasks = TODO.objects.filter(user=request.user).values()
        tasks_list = list(tasks)  # Convert QuerySet to a list of dictionaries
        data = json.dumps(tasks_list, cls=DjangoJSONEncoder)  # Serialize to JSON
        return HttpResponse(data, content_type='application/json')


def specific_task(request, task_id):
    if request.user.is_authenticated:
        task = get_object_or_404(TODO, pk=task_id, user=request.user)
        data = model_to_dict(task)
        return JsonResponse(data)
