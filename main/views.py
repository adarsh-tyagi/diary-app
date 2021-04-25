from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import NewUserForm, EntryForm
from .models import Entry
from datetime import datetime

# Create your views here.
#####################################
# username: admin , password: admin #
#####################################


def home(request):
    return render(request, template_name='main/home.html')

def register_view(request):
    if request.method == 'GET':
        return render(request, 'main/register.html', {"form": NewUserForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('main:home')
            except IntegrityError:
                return render(request, 'main/register.html', {'form': NewUserForm(), 'error': 'Username/email already registered!!!'})
        else:
            return render(request, 'main/register.html', {'form': NewUserForm(), 'error': 'Both passwords did not matched!!!'})

def login_view(request):
    if request.method == 'GET':
        return render(request, 'main/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'main/login.html', {'form': AuthenticationForm(), 'error': 'Username and password did not matched!!!'})
        else:
            login(request, user)
            return redirect('main:home')

@login_required
def logout_view(request):
    logout(request)
    return redirect("main:home")

@login_required
def entry_add(request):
    if request.method == 'GET':
        return render(request, 'main/entry_add.html', {'form': EntryForm()})
    else:
        try:
            form = EntryForm(request.POST)
            new_entry = form.save(commit=False)
            new_entry.user = request.user
            new_entry.save()
            return redirect('main:entries')
        except Exception as e:
            return render(request, 'main/entry_add.html', {'form': EntryForm(), 'error': 'Some error occurred!!!'})

@login_required
def entries_view(request):
    entries = Entry.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(entries, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/entries.html', {'entries': entries, 'count': len(entries), 'page_obj': page_obj})

@login_required
def entry_view(request, entry_pk):
    entry = get_object_or_404(Entry, pk=entry_pk, user=request.user)
    if request.method == 'GET':
        form = EntryForm(instance=entry)
        return render(request, 'main/entry.html', {'entry': entry, 'form': form})
    else:
        try:
            form = EntryForm(request.POST, instance=entry)
            form.save()
            return redirect('main:entries')
        except ValueError:
            return render(request, 'main/entry.html', {'entry': entry, 'form': form, 'error': 'Entry does not exist!!!'})

@login_required
def entry_delete(request, entry_pk):
    entry = get_object_or_404(Entry, pk=entry_pk, user=request.user)
    entry.delete()
    return redirect('main:entries')