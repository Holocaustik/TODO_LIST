from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import TodoForm
from .models import Todo

'''Переход пользователя на домашнюю страницу'''


def home(request):
    return render(request, 'todo/home.html')


'''Регистрация пользователя'''


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(),
                                                                'error': 'Данное имя уже занято.'})
        else:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(),
                                                            'error': 'Пароли не совпадают.'})


'''Вход пользователя'''


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html',
                          {'form': AuthenticationForm(),
                           'error': 'username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttodos')


'''Выход из учетной записи пользователя'''


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


'''Создание задачи на фронте'''


@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(),
                                                            'error': 'Вы ввели слишком много символов в заголовок. Попробуйти придумать название короче.'})


'''Переход на страницу всех задач'''


@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, end_date__isnull=True)
    todosend = Todo.objects.filter(user=request.user, end_date__isnull=False).order_by('end_date')
    todostatus_imp = Todo.objects.filter(user=request.user, end_date__isnull=True,
                                         status='Срочно')  # Список срочных невыполненных задач
    todostatus_simp = Todo.objects.filter(user=request.user, end_date__isnull=True,
                                          status='Очень срочно')  # Список очень срочных невыполненных задач
    todostatus_nimp = Todo.objects.filter(user=request.user, end_date__isnull=True,
                                          status='Не срочно')  # Список Не срочных невыполненных задач
    my_todos = {'todos': todos,
                'todosend': todosend,
                'todostatus_imp': todostatus_imp,
                'todostatus_simp': todostatus_simp,
                'todostatus_nimp': todostatus_nimp}
    return render(request, 'todo/currenttodos.html', {'my_todos': my_todos})


'''Переход на страницу задачи'''


@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo': todo,
                                                      'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo': todo,
                                                          'form': form,
                                                          'error': 'Неправильная информация'})


@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, end_date__isnull=False).order_by('-end_date')
    return render(request, 'todo/completedtodos.html', {'todos': todos})


'''Завершение задачи'''


@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.end_date = timezone.now()
        todo.save()
        return redirect('currenttodos')


'''Удаление задачи'''


@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')


