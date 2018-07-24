from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
def main(request):
    return render(request, 'login/login.html')