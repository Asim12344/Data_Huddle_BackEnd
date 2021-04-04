from django.urls import path
from .views import GetData,GetDataOfPreviousDays

urlpatterns = [
    path('getData', GetData.as_view()),
    path('getPrevData',GetDataOfPreviousDays.as_view())
]