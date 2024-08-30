

def extract_keywords(image_desc:str):
    
    # Split the description to find the keywords section
    if "**키워드 추출:**" in image_desc:
        keywords_section = image_desc.split("**키워드 추출:**")[1]
        # Split the keywords section into individual keywords
        keywords_list = [keyword.strip('- ').strip() for keyword in keywords_section.split('\n') if keyword.strip()]
        return keywords_list
    else:
        return [] 