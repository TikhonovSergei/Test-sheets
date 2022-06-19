
from django.conf import settings
from celery import shared_task
from .celery import app
import httplib2 
import apiclient
from datetime import datetime
import requests
from lxml import etree
from oauth2client.service_account import ServiceAccountCredentials
from .models import *
 
@shared_task
@app.task
def read_sheet():
    '''Задача чтения файла'''
     # Читаем ключи из файла
    credentials = ServiceAccountCredentials.from_json_keyfile_name(settings.CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

    httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API 
    spreadsheetId = '1lRw5N1dN6No8Ab-1xedFpQ1QOkowcrrB4lUlx3_6uLw'
    ranges = ["Лист номер один!A2:D1000"]
    results = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId,
                                        ranges = ranges,
                                        valueRenderOption = 'FORMATTED_VALUE',).execute() 
    result_values = results['valueRanges'][0]['values']
    order_lst = Orders.objects.all()
    order_number = {}
    add_order = {}
    for order in order_lst:
        add_order['data_deliveries'] = order.data_deliveries
        add_order['price_dolars'] = order.price_dolars
        order_number[order.number_order] = add_order
    responce = requests.post(url='http://www.cbr.ru/scripts/XML_daily.asp?')
    tree = etree.XML(responce.content)
    kurs = 57.5
    for val in result_values:
        rubles = int(val[2]) * kurs
        if val[1] in order_number:
            if order_number[val[1]]['price_dolars'] != val[2] or order_number[val[1]]['data_deliveries'] != datetime.strptime(val[3], "%d.%m.%Y").date():
                order = Orders.objects.get(number_order = val[1])
                order.price_dolars = val[2]
                order.price_rubles = rubles
                order.data_deliveries = datetime.strptime(val[3], "%d.%m.%Y").date()
                order.save()
        else:
            order = Orders(number = val[0], number_order = int(val[1]), price_dolars = val[2], price_rubles = rubles, data_deliveries = datetime.strptime(val[3], "%d.%m.%Y").date())
            order.save()

