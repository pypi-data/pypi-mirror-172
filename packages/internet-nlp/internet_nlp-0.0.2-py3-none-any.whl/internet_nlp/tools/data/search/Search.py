import requests
import urllib
from requests_html import HTML
from requests_html import HTMLSession
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import nltk
import sys
from pathlib import Path
sys.path.append(str(str(Path(__file__).parent.parent.parent) + "/normalizer"))
import Normalize

class SearchLinkData:

    def __init__(self):
        self.url = "https://google.com/search?q="
        self.headers = {
            'User-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
        }
        self.numOfRes = 10
        self.NTC = Normalize.NormalizeTextClass()

    def get_source(self, url):
        try:
            session = HTMLSession()
            response = session.get(url)
            return response
        except requests.exceptions.RequestException as e:
            print(e)

    def setQues(self, ques):
        self.ques = str(ques)
        self.url += urllib.parse.quote_plus(self.ques)
        self.url += "&num="
        self.url += str(self.numOfRes)
        response = self.get_source(self.url)
        links = list(response.html.absolute_links)
        google_domains = ('https://www.google.', 
                          'https://google.', 
                          'https://webcache.googleusercontent.', 
                          'http://webcache.googleusercontent.', 
                          'https://policies.google.',
                          'https://support.google.',
                          'https://maps.google.')
        for url in links[:]:
            if url.startswith(google_domains):
                links.remove(url)
        self.links = links

    def getWebsiteData(self):
        self.textFromWeb = []
        for url in self.links:
            req = Request(
                url=url,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            try:
                html = urlopen(url).read()
                soup = BeautifulSoup(html, features="html.parser")
                for script in soup(["script", "style"]):
                    script.extract()   
                text = str(soup.get_text())
                # lines = (line.strip() for line in text.splitlines())
                # chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                # text = '\n'.join(chunk for chunk in chunks if chunk)
                # self.NTC.setInputText(str(text))
                # self.NTC.doAllCommands()
                # text = self.NTC.getNormalizedText()
                text = text.replace('\n','')
                text = text.replace('\t','')
                text = text.replace("\'", '')
                text = text.replace('"', '')
                text = text.replace("\\", '')
                self.textFromWeb.append(text)
            except urllib.error.HTTPError as e:
                continue

    def getSentences(self):
        self.sentences = []
        for texts in self.textFromWeb:
            try:
                nltk.download('punkt')
                sentences = nltk.sent_tokenize(texts)  
                for i in sentences:
                    self.sentences.append(str(i))
            except Exception as e:
                print(e)
        return self.sentences
