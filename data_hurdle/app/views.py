from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
import sys, os
from django.conf import settings
import json
import requests
import datetime


class GetData(APIView):
    # permission_classes = (permissions.AllowAny, )
    def get(self, request, format=None):
        data = self.request.query_params
        try:
            company_name = data['companyName'] 
            yesterday_request = data['data'] 
            print("==================")
            print(yesterday_request)
            today_data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=24h')
            print(today_data.status_code)
            while today_data.status_code != 200:
                print("while")
                today_data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=24h')
                print(today_data.status_code)
            today_data = today_data.json()    
            if yesterday_request == "true":
                print("true")
                yesterday_data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=48h&before=24h')
                print(yesterday_data.status_code)
                while yesterday_data.status_code != 200:
                    print("while")
                    yesterday_data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=48h&before=24h')
                    print(yesterday_data.status_code)
                yesterday_data = yesterday_data.json() 
                return Response({'today_data': today_data['data'] , 'yesterday_data':yesterday_data['data']})
            return Response({'today_data': today_data['data']})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno , e)
            return Response({'error': e})

class GetDataOfPreviousDays(APIView):
    # permission_classes = (permissions.AllowAny, )
    def get(self, request, format=None):
        data = self.request.query_params
        try:
            company_name = data['companyName'] 
            counter = 1
            mentions = []
            date_array = []
            today_data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=24h')
            print(today_data.status_code)
            while today_data.status_code != 200:
                print("while")
                today_data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=24h')
                print(today_data.status_code)
            today_data = today_data.json()
            # today_data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=48h&before=24h').json()
            current_Date = datetime.datetime.today()
            # current_Date = datetime.datetime.today() - datetime.timedelta(days=counter)
            mentions.append(len(today_data['data']))
            date_array.append(str(current_Date)[0:10])
            after = 48
            before = 24
            while counter < 5:
                print(counter)
                data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=' + str(after) + 'h&before=' + str(before) + 'h')

                print("======== DATA =========")
                print(data.status_code)
                while data.status_code != 200:
                    print("while")
                    data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=' + str(after) + 'h&before=' + str(before) + 'h')
                    print(data.status_code)
                data = data.json()
                previous_Date = datetime.datetime.today() - datetime.timedelta(days=counter)
                mentions.append(len(data['data']))
                date_array.append(str(previous_Date)[0:10])
                after = after + 24
                before = before + 24
                counter = counter + 1 
            return Response({'today_data': today_data['data'] , 'mentions':mentions , 'dates': date_array})

            return Response({'today_data': "success"})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno , e)
            return Response({'error': e})

