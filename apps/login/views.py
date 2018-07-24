from django.shortcuts import render, HttpResponse, redirect
from .models import *

# Create your views here.
def main(request):
    return render(request, 'login/login.html')