from django.shortcuts import render, HttpResponse, redirect
from .models import *
import bcrypt

# Create your views here.
def login(request):
    return render(request, 'login/login.html')

def process_login(request):
    if request.method == 'POST':
        return redirect('/main')
    else:
        return redirect('/')

def register(request):
    return render(request, 'login/register.html')

def process_reg(request):
    if request.method == 'POST':
        return redirect('/register/pick_class')
    else:
        return redirect('/')

def pick_class(request):
    return render(request, 'login/pick_class.html')

def process_pick(request):
    if request.method == 'POST':
        return redirect('/main')
    else:
        return redirect('/')

def main(request):
    return render(request, 'login/main.html')

def display_player(request, id):
    return render(request, 'login/display_player.html')
    
def logout(request):
    if request.method == 'POST':
        return redirect('/')
    else:
        return redirect('/') 

def start_game(request):
    if request.method == 'POST':
        return redirect('/game_sess')
    else:
        return redirect('/') 

def game_sess(request):
    return render(request, 'login/game.html')

def attack(request):
    if request.method == 'POST':
        return redirect('/main')
    else:
        return redirect('/')

def leave(request):
    if request.method == 'POST':
        return redirect('/main')
    else:
        return redirect('/')