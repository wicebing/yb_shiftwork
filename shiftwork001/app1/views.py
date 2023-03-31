from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
def index(request):
    return render(request, 'app1/index.html')

def var(request):
    lists = ['Java','Python','C','C#','JS']
    dicts = {'name':'Tom','age':18, 'sex':'male'}
    return render(request, 'app2/var.html', {'lists':lists, 'dicts':dicts})