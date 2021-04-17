from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
import sys, os
from django.conf import settings
import json
import requests
import datetime


class GetData(APIView):
    permission_classes = (permissions.AllowAny, )
    def get(self, request, format=None):
        data = self.request.query_params
        try:
            company_name = data['companyName'] 
            print("==================")
            today_data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=24h')
            yesterday_data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=48h&before=24h')
            # today_data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=48h&before=24h')
            # yesterday_data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=72h&before=48h')
            today_data = today_data.json()    
            yesterday_data = yesterday_data.json() 
            return Response({'today_data': today_data['data'] , 'yesterday_data':yesterday_data['data']})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno , e)
            return Response({'error': e})

class GetDataOfPreviousDays(APIView):
    permission_classes = (permissions.AllowAny, )
    def get(self, request, format=None):
        data = self.request.query_params
        try:
            company_name = data['companyName'] 
            counter = 1
            mentions = []
            date_array = []
            today_data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=24h').json()
            # today_data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=48h&before=24h').json()
            current_Date = datetime.datetime.today()
            # current_Date = datetime.datetime.today() - datetime.timedelta(days=counter)
            mentions.append(len(today_data['data']))
            date_array.append(str(current_Date)[0:10])
            after = 48
            before = 24
            while counter < 10:
                print(counter)
                data = requests.get('https://api.pushshift.io/reddit/comment/search/?q='+company_name +'&after=' + str(after) + 'h&before=' + str(before) + 'h').json()
                previous_Date = datetime.datetime.today() - datetime.timedelta(days=counter)
                mentions.append(len(data['data']))
                date_array.append(str(previous_Date)[0:10])
                after = after + 24
                before = before + 24
                counter = counter + 1 
            return Response({'today_data': today_data['data'] , 'mentions':mentions , 'dates': date_array})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno , e)
            return Response({'error': e})

