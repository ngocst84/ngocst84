from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.detail import DetailView

import requests
from bs4 import BeautifulSoup
import os
import random
# from selenium.webdriver.common.keys import Keys
from selenium import webdriver
# import chromedriver_binary  # Adds chromedriver binary to path
# from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from django.core.paginator import Paginator
from .models import nfNews 
from .models import nfSpeech
from .models import nEBAYDATA
import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
from django.views import generic

from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
from ebaysdk.shopping import Connection as Shopping
from django.conf import settings

# Create your views here.

# class IndexView(generic.ListView):
#     template_name = 'crawldata/index.html'
class IndexView():

    def index(request):
        # return HttpResponse("Hello, world. You're at the polls index." + strftime("%z", gmtime()))
        context = {
            'test': 'test',
        }
        return render(request,"zplus/index.html",context)

    def getdataebay(self,request):
        dt1 = self.do()
        return HttpResponse(dt1)

    def getdata(ebaylink,ScrollNumber):
        driver = webdriver.Chrome()
        # driver = webdriver.Chrome(ChromeDriverManager().install())
        # driver = webdriver.Chrome(executable_path='C:/Users/ngocs/OneDrive/Desktop/Ngoc-Zplus/chromedriver.exe')
        driver.get (ebaylink)
        for i in range(1,ScrollNumber):
            driver.execute_script("window.scrollTo(1,10000)")
            time.sleep(3)
        # print (driver.page_source)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        items = soup.findAll('li', class_='s-item s-item--large s-item--bgcolored')
        # for it in items:
        #     ts = [link.find('a').text for link in titles]
        # ts = [link.find('h3').text for link in items]
        # print(items)    
        # driver.close()
        driver.quit()
        return items
    def showdata(edatas):
        i=0
        for ed in edatas:
            i+=1
        print (str(i) + '.'+ ed)

    def setItem(item):
        # print(item)
        title = "" if item.find('h3') == None else item.find('h3').text
        srcImage="" if item.find('img').attrs["src"] == None else item.find('img').attrs["src"]
        link = "" if item.find('a',attrs={'class':'s-item__link'}).attrs["href"] == None else item.find('a',attrs={'class':'s-item__link'}).attrs["href"]
        price = "" if item.find('span',attrs={'class':'s-item__price'}) == None else item.find('span',attrs={'class':'s-item__price'}).text
        trendingprice = "" if item.select_one("div > span.s-item__trending-price") == None else item.select_one("div > span.s-item__trending-price").text
        logistic = "" if item.find('span',attrs={'class':'s-item__shipping s-item__logisticsCost'}) == None else item.find('span',attrs={'class':'s-item__shipping s-item__logisticsCost'}).text
        sold = "" if item.find('span',attrs={'class':'s-item__hotness s-item__itemHotness'}) == None else item.find('span',attrs={'class':'s-item__hotness s-item__itemHotness'}).text
        cetified = "" if item.select_one("span.s-item__certified-refurbished-badge") == None else item.select_one("span.s-item__certified-refurbished-badge").text
        star = "" if item.select_one("div.b-starrating > span") == None else item.select_one("div.b-starrating > span").text
        countreview = "" if item.select_one("span.s-item__reviews-count > span") == None else item.select_one("span.s-item__reviews-count > span").text
        return [title,srcImage,link,price,trendingprice,logistic,sold,star,countreview]

    # showdata(getdata("https://www.ebay.com/b/PC-Laptops-Netbooks/177/bn_317584"))
    # print (getdata("https://www.ebay.com/b/PC-Laptops-Netbooks/177/bn_317584")

    def do(self):
        i=0
        dtw = list()
        # for dt in getdata("https://www.ebay.com/b/PC-Laptops-Netbooks/177/bn_317584"):
        for dt in self.getdata("https://www.ebay.com/sch/PC-Laptops-Netbooks/177/m.html?_ssn=antonline&_dcat=177&rt=nc&_mPrRngCbx=1&_udlo=400&_udhi=1200"):
            i+=1
            dtw.append(setItem(dt))
            if (i>3):
                break
        return dtw

    # dt1 = do()
    # with open('listfile.txt', 'w') as filehandle:
    #     json.dump(dt1, filehandle)
    #     print(dt1)
        
    def readweb(request):
        obj = nfNews("https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FuWnBHZ0pXVGlnQVAB/sections/CAQiTENCQVNNd29JTDIwdk1EVnFhR2NTQW5acEdnSldUaUlQQ0FRYUN3b0pMMjB2TURGamNtUTFLZzRLREJJS1Ztbmh1NGQwSUU1aGJTZ0EqKggAKiYICiIgQ0JBU0Vnb0lMMjB2TURWcWFHY1NBblpwR2dKV1RpZ0FQAVAB?hl=vi&gl=VN&ceid=VN%3Avi",1).getGGnews()
        sp = []
        for t1 in obj:
            sp.append(nfSpeech(t1,"ms"))
        paginator= Paginator(sp,7)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context={"page_obj":page_obj}
        return render(request,"zplus/readweb.html",context)

    def ebayapi(request):
    
        try:
            api = Connection(appid='58.187.21.161', config_file=None)
            response = api.execute('findItemsAdvanced', {'keywords': 'legos'})

            assert(response.reply.ack == 'Success')
            assert(type(response.reply.timestamp) == datetime.datetime)
            assert(type(response.reply.searchResult.item) == list)

            item = response.reply.searchResult.item[0]
            assert(type(item.listingInfo.endTime) == datetime.datetime)
            assert(type(response.dict()) == dict)
            arr = response.dict()
            arr = response.dict()
        except ConnectionError as e:
            arr = e.response.dict()
        # print(e)
        # print(e.response.dict())
        context={"arr":arr}
        return render(request,"zplus/ebayapi.html",context)
    def getdataebay3(request, question_id):
            arr = nEBAYDATA()
            arr.title = "abc"
            arr.link = "bcdef"
            return render(request, 'zplus/nebaydata.html', {'arr': arr,'now':"abcd"})

class ViewEbay(generic.TemplateView):
    # def getdataebay2(request):
    #     arr = []

    #     context={"arr":arr}
    #     return render(request,"zplus/getdataebay2.html",context)
    # model = Article
    # paginate_by = 100  # if pagination is desired

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['now'] = timezone.now()
    #     return context
    
    template_name = 'zplus/nebaydata5.html'

    def __init__(self):
        # Initialization of the Strings
        # obj = self.getdata("https://www.ebay.com/b/PC-Laptops-Netbooks/177/bn_317584",1)


        # obj = self.getdata("https://www.ebay.com/b/Dell-Laptops-Netbooks/175672/bn_2780156",1)
        now = datetime.datetime.now()


        # self.extra_context = {'now': now,'obj':obj}

    def getdata(self,link,ScrollNumber):
        # driver = webdriver.Chrome(executable_path='E:/O-N/OneDrive/Desktop/Ngoc-Zplus/chromedriver.exe')
        # driver = webdriver.Chrome(executable_path='C:/Users/ngocs/OneDrive/Desktop/Ngoc-Zplus/chromedriver.exe')
        driver = webdriver.Chrome()
        driver.get (link)
        for i in range(1,ScrollNumber):
            driver.execute_script("window.scrollTo(1,50000)")
            time.sleep(2)
        # print (driver.page_source)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        items = soup.findAll('li', class_='s-item s-item--large s-item--bgcolored')
        eb = []
        for it in items:
            eb.append(self.setItem(it))            
        driver.close()
        driver.quit()
        return eb
    def setItem(self,item):
        # print(item)
        edt = nEBAYDATA()
        edt.title = "" if item.find('h3') == None else item.find('h3').text
        edt.srcImage="" if item.find('img').attrs["src"] == None else item.find('img').attrs["src"]
        edt.link = "" if item.find('a',attrs={'class':'s-item__link'}).attrs["href"] == None else item.find('a',attrs={'class':'s-item__link'}).attrs["href"]
        edt.price = "" if item.find('span',attrs={'class':'s-item__price'}) == None else item.find('span',attrs={'class':'s-item__price'}).text
        edt.trendingprice = "" if item.select_one("div > span.s-item__trending-price") == None else item.select_one("div > span.s-item__trending-price").text
        edt.logistic = "" if item.find('span',attrs={'class':'s-item__shipping s-item__logisticsCost'}) == None else item.find('span',attrs={'class':'s-item__shipping s-item__logisticsCost'}).text
        edt.sold = "" if item.find('span',attrs={'class':'s-item__hotness s-item__itemHotness'}) == None else item.find('span',attrs={'class':'s-item__hotness s-item__itemHotness'}).text
        edt.cetified = "" if item.select_one("span.s-item__certified-refurbished-badge") == None else item.select_one("span.s-item__certified-refurbished-badge").text
        edt.star = "" if item.select_one("div.b-starrating > span") == None else item.select_one("div.b-starrating > span").text
        edt.countreview = "" if item.select_one("span.s-item__reviews-count > span") == None else item.select_one("span.s-item__reviews-count > span").text
        return edt
    
    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        # self.template_name = 'https://www.google.com/'
        return render(request, self.template_name, self.extra_context)
    def post(self, request, *args, **kwargs):
        results = None
        query_keywords = ""
        countresult = 0
        if request.method == 'POST':
            try:
                post_data = dict()
                post_data = request.POST
                query_keywords = str(post_data['keywords'])
                if query_keywords:
                    ebayyaml = getattr(settings, "EBAYSETTING", None)
                    api = Connection(config_file= ebayyaml)
                    # api = Shopping(config_file= ebayyaml)
                    rs = api.execute('findItemsAdvanced', {'keywords': query_keywords})
                    results = rs.dict().get('searchResult')
                    # results = obj.dict2obj(dt)
                    results = list(results['item'])
                    countresult = len(results)
            except ConnectionError as e:
                print(e)
                print(e.response.dict())
        self.extra_context = {'obj':results,'countresult':countresult,'keywords_result':query_keywords}
        return render(request, self.template_name, self.extra_context)