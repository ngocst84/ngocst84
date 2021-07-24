from django.db import models

# Create your models here.
import os
from re import S
import requests
from bs4 import BeautifulSoup
import pyttsx3
import gtts
from playsound import playsound
from selenium import webdriver
import time
from io import BytesIO
from urllib.parse import quote

from pydub import AudioSegment
# from pydub.playback import play

class nfNews ():
    def __init__(self, link, numberscroll = 5):
        # self.executable_path='C:/Users/ngocs/OneDrive/Desktop/Ngoc-Zplus/chromedriver.exe'
        self.executable_path='E:/O-N/OneDrive/Desktop/Ngoc-Zplus/chromedriver.exe'
        self.link = link
        self.numberscroll = numberscroll
    
    def getGGnews(self):
        driver = webdriver.Chrome(self.executable_path)
        driver.get (self.link)
        for i in range(1,self.numberscroll):
            driver.execute_script("window.scrollTo(1,5000)")
            time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        titles = soup.findAll('h3', class_='ipQwMb ekueJc RD0gLb')
        ts = [lk.find('a').text for lk in titles]
        # driver.close()
        driver.quit()
        return ts
    def getnewsdetail(self):
        blacklist = [
            'style',
            'script',
            # other elements,
            ]
        whitelist = [
            'p'
            ]
        url = self.link
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')
        # text_elements = [t for t in soup.find_all(text=True) if t.parent.name not in blacklist]
        text_elements = soup.find('section',class_="enter-24h-cate-article")
        # print (str(text_elements))
        t1 = [t for t in BeautifulSoup(str(text_elements),'html.parser').find_all(text=True) if t.parent.name not in blacklist]
        # titles = soup.findAll('section', class_='enter-24h-cate-article')
        # ts = [te.find('a').text for te in text_elements]
        # ' '.join(t1).split()
        # print (t1)
        return list(filter(lambda x: len(x) > 1, t1))
        # for t2 in t3:
            # print(type(t2))
            # print (len(t2))
            # print (str(t2))


    def speechgglink(self):
        i=0
        for t1 in self.getGGnews():
            i+=1
            print (str(i) + '.'+ t1)
            if (i % 2):
                nfSpeech(t1,"ms").speechtext()
            else:
                nfSpeech(t1,"gg").speechtext()
            if (i >6): break
    def speechdetail(self):
            i=0
            for t1 in self.getnewsdetail():
                i+=1
                print (str(i) + '.'+ t1)
                nfSpeech(t1,"ms").speechtext()

class nfSpeech ():
    def __init__(self, text,voice = "ms"):
        self.text = text
        self.voice = voice
        self.link = 'https://translate.google.com.vn/translate_tts?ie=UTF-8&q='+ quote(text) +'&tl=vi&client=tw-ob'
        self.mp3= self.synthesize_text()
        # self.mp3= ""

    def speechtext(self):
            if (self.voice == "ms"):
                engine = pyttsx3.init()
                # Use male Vietnam voice
                vi_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_viVN_An"
                engine.setProperty('voice', vi_voice_id)
                engine.setProperty('rate', 200)     # setting up new voice rate
                engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
                engine.say(self.text)
                engine.runAndWait()
                engine.stop()
            else:
               
                tts = gtts.gTTS(self.text, lang ="vi", slow = False)
                # mp3_fp = BytesIO()
                # tts.write_to_fp(mp3_fp)
                # mp3_fp.seek(0)
                # song = AudioSegment.from_file(mp3_fp, format="mp3")
                # play(song)
                # playsound(mp3_fp.)
                # mp3_fp.close
                tts.save("tmp.mp3")
                playsound("tmp.mp3")
                os.remove("tmp.mp3")
    def synthesize_text(self):
        tts = gtts.gTTS(self.text, lang ="vi", slow = False)
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        song = AudioSegment.from_mp3(mp3_fp)
        return song
    def __str__(self):
            return self.text

class Song(models.Model):
    title= models.TextField()
    artist= models.TextField()
    image= models.ImageField()
    audio_file = models.FileField(blank=True,null=True)
    audio_link = models.CharField(max_length=200,blank=True,null=True)
    duration=models.CharField(max_length=20)
    paginate_by = 2

    def __str__(self):
        return self.title
class nEBAYDATA(models.Model):
    title = models.TextField()
    srcImage = models.CharField(max_length=200,blank=True,null=True)
    link = models.CharField(max_length=200,blank=True,null=True)
    price = models.ImageField()
    trendingprice = models.TextField()
    logistic = models.TextField() 
    sold = models.TextField() 
    cetified = models.TextField()
    star = models.TextField()  
    countreview = models.TextField()
    
    def __str__(self):
        return self.title
