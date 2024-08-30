from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

import pandas as pd 
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
import re 
import requests
from bs4 import BeautifulSoup
import urllib.parse
import get_article


# 공통 전처리 함수 
def clean_text_common(content):
    # 공통 전처리 로직 구현
    # # 불필요한 텍스트 및 특수 문자 제거
    content = re.sub(r'\[.*?\]', '', content)  # [사진 출처]와 같은 부분 제거
    content = re.sub(r'\n+', '\n', content)  # 여러 줄바꿈을 하나로 축소
    content = re.sub(r'\s+', ' ', content)  # 여러 공백을 하나로 축소
    content = re.sub(r'[▶■]', '', content)  # 특수 문자 제거
    content = content.replace('\\', '')  # 백슬래시 제거
    # "주소" 이하의 문자열 제거
    content = re.sub(r'주소.*', '', content)
    # "#" 구문과 그 이후의 문자열 제거
    content = re.sub(r'#.*', '', content, flags=re.DOTALL) 
    # "프린트 스크랩 url복사" 구문과 그 앞의 문자열 제거
    content = re.sub(r'.*프린트 스크랩 url복사', '', content, flags=re.DOTALL)
    # "- 더보기" 구문과 그 앞의 문자열 제거
    content = re.sub(r'.*- 더보기', '', content, flags=re.DOTALL)
    # "사진" 구문과 그 이후의 문자열 제거 (중간 중간 사진 포함돼있음) 
    #content = re.sub(r'\(사진.*', '', content, flags=re.DOTALL)
    # "◎" 구문과 그 이후의 문자열 제거
    content = re.sub(r'◎.*', '', content, flags=re.DOTALL)
    
    
    
    content = content.strip() 
    
    return content



# 기사 원문 
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


def get_article_cleaned(contents_keyword, article_index):
    
    articles = get_article.search_naver_news(contents_keyword) 
    
    title = articles[article_index][0] # articles 첫번째 기사 제목
    link = articles[article_index][1]
    
    article_raw = get_news(link) 
    article_cleaned = clean_text_common(article_raw) 
    
    # 전처리된 기사 텍스트 리턴 
    return article_cleaned, title
    
