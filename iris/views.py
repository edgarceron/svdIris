from django.shortcuts import render

def check_iris(request):
    return render(request, 'iris/check_iris.html')

def check_iris2(request):
    return render(request, 'iris/check_iris2.html')