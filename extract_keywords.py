

def extract_keywords(img_str):
    # 키워드 추출 부분을 찾기
    keyword_section = img_str.split('### 키워드')[1]
    
    # 키워드를 줄 단위로 분리하고, 앞뒤 공백 제거
    keywords = [keyword.strip('- ').strip() for keyword in keyword_section.split('\n') if keyword.strip()]
    
    return keywords