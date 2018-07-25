from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def login(request):
    return render(request, 'login/login.html')

def process_login(request):
    if request.method == 'POST':
        errors = Player.objects.login_validation(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        request.session['id'] = Player.objects.get(email = request.POST['email']).id
        request.session['username'] = Player.objects.get(email = request.POST['email']).username  
        if Player.objects.get(email = request.POST['email']).role == -1:
            return redirect('/register/pick_class')

        request.session['logged_in'] = True

        return redirect('/main')
    else:
        return redirect('/')

def register(request):
    return render(request, 'login/register.html')

def process_reg(request):
    if request.method == 'POST':
        errors = Player.objects.reg_validation(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')
        
        player = Player(username = request.POST['username'], email = request.POST['email'], pass_hs= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()), level = 1, role = -1)
        player.save()
        request.session['id'] = player.id
        request.session['name'] = player.username

        return redirect('/register/pick_class')
    else:
        return redirect('/')

def pick_class(request):
    return render(request, 'login/pick_class.html')

def process_pick(request):
    if request.method == 'POST':

        player = Player.objects.get(id = request.session['id'])
        if request.POST['role'] == 'knight':
            player.role = 1
        elif request.POST['role'] == 'rogue':
            player.role = 2
        elif request.POST['role'] == 'mage':
            player.role = 3
        elif request.POST['role'] == 'ranger':
            player.role = 4
        elif request.POST['role'] == 'beserker':
            player.role = 5
        player.save()

        request.session['logged_in'] = True
        return redirect('/main')
    else:
        return redirect('/')

def main(request):
    return render(request, 'login/main.html')

def display_player(request, id):
    return render(request, 'login/display_player.html')

def logout(request):
    if request.method == 'POST':
        request.session.clear()
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