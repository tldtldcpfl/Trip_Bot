from rerank.utils import model, tokenizer, exp_normalize   
from rerank.web_search import get_news  
import torch 


# Reranker를 사용한 순위 조정 함수
def rerank_articles_by_scores(query_sentence, article_links, top_k=5): 
    """
    질의와 기사 원문 간의 유사도를 기반으로 문서 순위를 재조정

    Args:
        query_sentence (str): 사용자 질의 (문장 단위)
        article_links (list): 기사 링크 리스트
        top_k (int): 분석할 기사 개수

    Returns:
        list: 재정렬된 (기사 제목, 기사 링크, 기사 원문, 유사도 점수) 리스트
    """
    articles_content = [] 

    # 각 링크에서 기사 원문 가져오기
    for link in article_links[:top_k]:
        content = get_news(link)   # 기사 원문 리턴 
        if content:  # 원문이 비어있지 않으면 추가
            articles_content.append((link, content))   
    
    if not articles_content:  
        print("기사 원문을 가져올 수 없습니다.")
        return []

    # 질의와 기사 원문 유사도 계산
    pairs = [(query_sentence, content) for _, content in articles_content]

    with torch.no_grad():
        inputs = tokenizer(pairs, padding=True, truncation=True, return_tensors='pt', max_length=512)
        scores = model(**inputs, return_dict=True).logits.view(-1, ).float()
        scores = exp_normalize(scores.numpy())

    # 유사도 점수를 기반으로 재정렬
    ranked_articles = sorted(zip(articles_content, scores), key=lambda x: x[1], reverse=True)

    return [(link, content, score) for ((link, content), score) in ranked_articles]



# 유사도 점수 계산
def get_similarity_scores(query, articles, is_rerank):
    """
    질의와 기사 원문 간의 유사도 점수를 계산합니다.

    Args:
        query (str): 사용자 질문.
        articles (list): 기사 원문 리스트 [(link, content)].
        is_rerank (bool): True면 정렬 수행, False면 점수만 반환.

    Returns:
        list: 유사도 점수 리스트.
    """
    pairs = [(query, content) for _, content in articles]
    
    with torch.no_grad():
        inputs = tokenizer(pairs, padding=True, truncation=True, return_tensors='pt', max_length=512)
        scores = model(**inputs, return_dict=True).logits.view(-1, ).float()
        scores = exp_normalize(scores.numpy()) 
    
    # is_rank = True이면  scores 높은 순으로 문서 순서 정렬 
    if is_rerank:
        scores = sorted(scores, reverse=True)   
        
    return scores  
