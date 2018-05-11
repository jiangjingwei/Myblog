from django.shortcuts import render

# Create your views here.


def index(request):

    return render(request, 'blog/index.html')


def log_in(request):

    return render(request, 'blog/login.html')


def register(request):

    return render(request, 'blog/register.html')
