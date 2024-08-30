import os
import dotenv
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load .env file in local dir 
dotenv.load_dotenv('your/local/path/AOAI.env')

def get_api_info(api_name):
    
    if api_name == 'gpt-4o-mini':
        gpt4o_mini_key = os.getenv('OPENAI_API_KEY_USEA')
        gpt4o_mini_endpoint = os.getenv('OPENAI_AZURE_ENDPOINT_USEA')
        return gpt4o_mini_key, gpt4o_mini_endpoint
    
    elif api_name == 'gpt-4o' or api_name == 'gpt-35-turbo':
        openai_key = os.getenv('OPENAI_API_KEY_AUEA')
        openai_endpoint = os.getenv('OPENAI_AZURE_ENDPOINT_AUEA')
        return openai_key, openai_endpoint
    
    else:
        raise ValueError(f"Unknown API name: {api_name}")


# Choose api_name    
def get_client(api_key, api_endpoint):
    client = AzureOpenAI( 
        api_key = api_key,  
        azure_endpoint = api_endpoint, 
        api_version = "2024-02-01") 

    return client
