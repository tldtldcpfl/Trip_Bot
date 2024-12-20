# from langchain.document_loaders import WebBaseLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pandas as pd 
import re 
import requests
from bs4 import BeautifulSoup 

from langchain.text_splitter import CharacterTextSplitter
# from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate



# 뉴스 검색 API를 사용하여 기사 제목 검색
def search_naver_news(contents_keyword):
    
    url = f"https://search.naver.com/search.naver?where=news&query={contents_keyword}&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=1&refresh_start=0&related=0&press_paper=009"
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    articles = []
    for item in soup.select('a.news_tit'):
        title = item.get('title')
        link = item.get('href')
        
        articles.append((title, link))
    
    return articles 


# 기사 원문 리턴 
def get_news(news_page):
    web_loader = WebBaseLoader([news_page]) 
    data = web_loader.load()
    
    if not data:
        print(f'No content found for URL: {news_page}')
        return ""
    
    news_dict = data[0].dict()
    #content = news_dict['page_content']
    content = news_dict.get('page_content', "")
    
    return content 

