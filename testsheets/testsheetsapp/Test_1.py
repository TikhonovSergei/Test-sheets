# Подключаем библиотеки
from unicodedata import decimal
import httplib2 
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
import sys
sys.path.append(r"/Users/janinatikhonova/Documents/GitHub/Test-sheets/testsheets/")
#from testsheetsapp.models import *

CREDENTIALS_FILE = 'fleet-standard-351108-f4a1a791c631.json' 

# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API 
spreadsheetId = '1lRw5N1dN6No8Ab-1xedFpQ1QOkowcrrB4lUlx3_6uLw'
ranges = ["Лист номер один!A2:D1000"]
results = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId,
                                    ranges = ranges,
                                     valueRenderOption = 'FORMATTED_VALUE',  
                                     dateTimeRenderOption = 'FORMATTED_STRING').execute() 
result_values = results['valueRanges'][0]['values']
for val in result_values:
    kurs = float(57.5)
    rubles = float(val[2]) * kurs
    print(val, val[2], rubles)
    #order = Orders(number = val[0], number_order = val[1], price_dolars = val[2], price_rubles = rubles, data_deliveries = val[3])
    #order.save()
