from .models import nEBAYDATA
from django.urls import path

from . import views
from .views import ViewEbay
from .views import IndexView

app_name = 'crawldata'
urlpatterns = [
    path('', IndexView.index, name='index'),
    path('getdataebay/', IndexView.getdataebay, name='getdataebay'),
    path('readweb/', IndexView.readweb, name='readweb'),
    path('ebayapi/', IndexView.ebayapi, name='ebayapi'),
    path('getdataebay3/<int:pk>/', ViewEbay.as_view(), name='nebaydata'),
    path('getdataebay5/', ViewEbay.as_view(), name='search'),
    # path('getdataebay3/<int:question_id>/', views.getdataebay3, name='getdataebay3'),
]