import torch 

from utils import model, tokenizer, exp_normalize   
from web_search import search_naver_news, get_news  
from reranker import rerank_articles_by_scores, get_similarity_scores
from web_search import search_naver_news, get_news  


# 사용자 입력
#user_query_sentence = input("질문을 입력해주세요 (문장 단위): ")
user_query = "요즘 주택 청약 관련 소식이 궁금해요"  
contents_keyword = '주택 청약'

# 기사 검색 및 원문 기반 재정렬
articles = search_naver_news(contents_keyword)  
article_links = [link for _, link in articles]

ranked_articles = rerank_articles_by_scores(user_query, article_links, top_k=5)

# 결과 출력
print("\n유사도 기반 재정렬 결과:")
for i, (link, content, score) in enumerate(ranked_articles):
    print(f"{i + 1}. 링크: {link}\n   유사도 점수: {score:.4f}\n")      
    

# 기사 원문 가져오기
articles = [(link, get_news(link)) for link in article_links[:10] if get_news(link)]

# Reranker 적용 전후 유사도 점수 계산
before_scores = get_similarity_scores(user_query, articles, is_rerank=False)
after_scores = get_similarity_scores(user_query, articles, is_rerank=True)  


mean_after_score = sum(after_scores[:5]) / len(after_scores)
mean_before_score = sum(before_scores[:5]) / len(before_scores)

# Rerank 적용 이후 유사도 값 증가 확인  
if mean_after_score > mean_before_score: 
    print(f'Rerank 적용 이후 상위 5개 문서와 쿼리간의 평균 유사도값 증가: + {round(mean_after_score - mean_before_score,2)}') 

    