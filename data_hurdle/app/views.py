from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
import sys, os
from django.conf import settings
import json
import requests
# import datetime
from datetime import datetime,timedelta

class GetData(APIView):
    # permission_classes = (permissions.AllowAny, )
    def get(self, request, format=None):
        data = self.request.query_params
        try:
            company_name = data['companyName'] 
            yesterday_request = data['data'] 
            print("=================")
            print(company_name)
            today_data_array = []
            yesterday_data_array = []
            today_data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=24h&size=1000')
            print(today_data.status_code)
            while today_data.status_code != 200:
                print("while")
                today_data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=24h&size=1000')
                print(today_data.status_code)
            today_data = today_data.json()    
            print(len(today_data['data']))
            today_data_array.extend(today_data['data'])
            current_Date = datetime.today()
            while len(today_data['data']) == 100:
                # current_Date = datetime.today()
                get_time = datetime.fromtimestamp(today_data['data'][len(today_data['data'])-1]['created_utc'])
                print(current_Date)
                print(get_time)
                subtract = current_Date - get_time
                print(subtract)
                subtract = str(subtract)
                print(subtract.split(":")[0])
                hour = int(subtract.split(":")[0]) + 1
                print(hour)
                today_data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after='+str(hour)+'h&size=1000')
                print(today_data.status_code)
                while today_data.status_code != 200:
                    print("while")
                    today_data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after='+str(hour)+'h&size=1000')
                    print(today_data.status_code)
                today_data = today_data.json()   
                print("====== Total Records ============")
                print(len(today_data['data']))
                today_data_array.extend(today_data['data'])
            print("====== today_data_array ============")
            print(len(today_data_array))
            if yesterday_request == "true":
                print("true")
                yesterday_data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=48h&before=24h&size=1000')
                print(yesterday_data.status_code)
                while yesterday_data.status_code != 200:
                    print("while")
                    yesterday_data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=48h&before=24h&size=1000')
                    print(yesterday_data.status_code)
                yesterday_data = yesterday_data.json() 
                print(len(yesterday_data['data']))
                yesterday_data_array.extend(yesterday_data['data'])
                previous_Date = datetime.today() - timedelta(days=2)
                print("=========== Process ==============")
                while len(yesterday_data['data']) == 100:
                    
                    get_time = datetime.fromtimestamp(yesterday_data['data'][len(yesterday_data['data'])-1]['created_utc'])
                    print(previous_Date)
                    print(get_time)
                    subtract = get_time - previous_Date
                    print(subtract)
                    subtract = str(subtract)
                    print(subtract.split(":")[0])
                    hour = int(subtract.split(":")[0]) + 1
                    print(hour)
                    hour =  48 - hour
                    print("==== Hour ===")
                    print(hour)
                    yesterday_data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=' + str(hour) + 'h&before=24h&size=1000')
                    print(yesterday_data.status_code)
                    while yesterday_data.status_code != 200:
                        print("while")
                        yesterday_data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=' + str(hour)+ 'h&before=24h&size=1000')
                        print(yesterday_data.status_code)
                    yesterday_data = yesterday_data.json()   
                    print("====== Total yesterday_data Records ============")
                    print(len(yesterday_data['data']))
                    yesterday_data_array.extend(yesterday_data['data'])
                print("====== yesterday_data_array ============")
                print(len(yesterday_data_array))
                return Response({'today_data': today_data_array , 'yesterday_data':yesterday_data_array})
            return Response({'today_data': today_data_array})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno , e)
            return Response({'error': e})

# class GetDataOfPreviousDays(APIView):
#     # permission_classes = (permissions.AllowAny, )
#     def get(self, request, format=None):
#         data = self.request.query_params
#         try:
#             company_name = data['companyName'] 
#             counter = 1
#             mentions = []
#             date_array = []
#             today_data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=24h')
#             print(today_data.status_code)
#             while today_data.status_code != 200:
#                 print("while")
#                 today_data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=24h')
#                 print(today_data.status_code)
#             today_data = today_data.json()
#             print(len(today_data['data']))
#             # today_data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=48h&before=24h').json()
#             current_Date = datetime.today()
#             # current_Date = datetime.datetime.today() - datetime.timedelta(days=counter)
#             mentions.append(len(today_data['data']))
#             date_array.append(str(current_Date)[0:10])
#             after = 48
#             before = 24
#             while counter < 5:
#                 print(counter)
#                 data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=' + str(after) + 'h&before=' + str(before) + 'h')

#                 print("======== DATA =========")
#                 print(data.status_code)
#                 while data.status_code != 200:
#                     print("while")
#                     data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=' + str(after) + 'h&before=' + str(before) + 'h')
#                     print(data.status_code)
#                 data = data.json()
#                 previous_Date = datetime.today() - timedelta(days=counter)
#                 mentions.append(len(data['data']))
#                 date_array.append(str(previous_Date)[0:10])
#                 after = after + 24
#                 before = before + 24
#                 counter = counter + 1 
#             return Response({'today_data': today_data['data'] , 'mentions':mentions , 'dates': date_array})

#             return Response({'today_data': "success"})
#         except Exception as e:
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             print(exc_type, fname, exc_tb.tb_lineno , e)
#             return Response({'error': e})

class GetDataOfPreviousDays(APIView):
    # permission_classes = (permissions.AllowAny, )
    def get(self, request, format=None):
        data = self.request.query_params
        try:
            company_name = data['companyName'] 
            print("==================")
            print(company_name)
            counter = 1
            mentions = []
            date_array = []
            today_data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=120h&size=1000')
            print(today_data.status_code)
            while today_data.status_code != 200:
                print("while")
                today_data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=120h&size=1000')
                print(today_data.status_code)
            today_data = today_data.json()
            i = 0
            obj = {}
            count = 1
            print(len(today_data['data']))
            for data in today_data['data']:
                get_time = datetime.fromtimestamp(data['created_utc'])
                get_time = str(get_time)[0:10]
                print(get_time)
                if i == 0:
                    obj[get_time] = count    
                    count = count + 1
                else:
                    if get_time == previous_date:
                        obj[get_time] = count 
                        count = count + 1
                    else:
                        count = 1
                        obj[get_time] = count
                        count = count + 1
                i = i + 1
                previous_date = get_time


            mentions = []
            date_array = []
            for o in obj:
                print(o)
                mentions.append(obj[o])
                date_array.append(o)
            print(mentions)
            print(date_array)
            return Response({'mentions':mentions , 'dates': date_array})

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno , e)
            return Response({'error': e})

