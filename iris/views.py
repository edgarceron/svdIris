from django.shortcuts import render

def check_iris(request):
    return render(request, 'iris/check_iris.html')