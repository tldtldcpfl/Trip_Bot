import get_api_key 
import encode_base64 


# 사용할 api_name 설정 
api_name = 'gpt-4o-mini' 
api_key, api_endpoint = get_api_key.get_api_info(api_name)
client = get_api_key.get_client(api_key, api_endpoint) 


def describe_img(image_path): 
    
    image = encode_base64.encode_image(image_path)
    
    response = client.chat.completions.create(
        model= api_name,
        messages=[
            {"role": "system", "content": "You are an AI assistant that analyzes images and provides detailed descriptions."},
            
            {"role": "user", "content": [
                {"type": "text", "text": "이미지 풍경에서 보이는 특징을 묘사해주세요. 아래에 키워드 추출:"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}}
            ]}
        ],
        max_tokens=300,
    )
    
    return response.choices[0].message.content