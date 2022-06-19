from django.shortcuts import render
from django.conf import settings
from .models import *

def index(request):
    '''Стартовая страница'''

    order_lst = Orders.objects.all()
    return render(request, 'testsheetsapp/index.html', { 'sheet_lst': order_lst})