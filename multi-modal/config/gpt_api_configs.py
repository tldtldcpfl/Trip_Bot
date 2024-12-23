import dotenv
from dotenv import load_dotenv
from openai import AzureOpenAI
import os
import requests
from io import BytesIO
import requests




#  .env 파일에 선언된 인자들을 불러오기
dotenv.load_dotenv('/home/your/local/path/AI.env')  
# 오스트레일리아 동부: gpt-4o, gpt-35-turbo
openai_key = os.getenv('OPENAI_API_KEY_AUEA') # api-key
openai_endpoint = os.getenv('OPENAI_AZURE_ENDPOINT_AUEA') # end point 


# api-key 
# 미국 동부: gpt-4o-mini  
gpt4o_mini_key = os.getenv('OPENAI_API_KEY_USEA')
gpt4o_mini_endpoint = os.getenv('OPENAI_AZURE_ENDPOINT_USEA')


# client 정의 
client = AzureOpenAI(
    api_key = gpt4o_mini_key,   
    azure_endpoint = gpt4o_mini_endpoint,
  #api_version = "2024-02-01" 
    api_version = '2024-08-01-preview'  # api 버전 업 
)  

