from django.shortcuts import render, HttpResponse, redirect
from .models import *
import bcrypt

# Create your views here.
def main(request):
    return render(request, 'login/login.html')

def register(request):
    return render(request, 'login/register.html')

def process_reg(request):
    if request.method == 'POST':
        return redirect('/register/pick_class')
    else:
        return redirect('/')

def pick_class(request):
    return render(request, 'login/pick_class.html')