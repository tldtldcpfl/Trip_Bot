from rerank.reranker import get_similarity_scores, rerank_articles_by_scores
from rerank.utils import model, tokenizer, exp_normalize   
from rerank.web_search import get_news, search_naver_news
from tqdm.notebook import tqdm 

from config.gpt_api_configs import client 

import os
os.environ['USER_AGENT'] = 'rank_agent'  


def search_articles(contents_keyword, top_k=5):
    print(f"네이버 뉴스 기사를 {top_k}건 검색 중입니다...")
    articles = search_naver_news(contents_keyword)
    return [link for _, link in articles]

def rerank_article_links(article_links, user_query, top_k=5):
    print("기사 링크를 재정렬 중입니다...")
    ranked_articles = []
    for link in tqdm(article_links, desc="기사 재정렬", unit="article"):
        try:
            ranked_result = rerank_articles_by_scores(user_query, [link], top_k=1)
            ranked_articles.extend(ranked_result)
        except Exception as e:
            print(f"Error processing link {link}: {e}")
    return ranked_articles[:top_k]

def summarize_article(article, model="gpt-4o"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"입력받은 기사 원문 {article}에서 특수 문자를 제거하고 주요 내용을 한글로 요약하세요."},
        ],
        max_tokens=800,
        temperature=0
    )
    return response.choices[0].message.content

def rerank_articles(contents_keyword, user_query, top_k=5):
    article_links = search_articles(contents_keyword, top_k)
    return rerank_article_links(article_links, user_query, top_k)

def doc_rank(func):
    def wrapper(contents_keyword, user_query, n):
        print(f'Rerank된 문서 중 {n+1}위 기사의 요약입니다.')
        result = func(contents_keyword, user_query, n)
        return result
    return wrapper

@doc_rank
def article_summary(contents_keyword, user_query, n: int) -> str:
    ranked_articles = rerank_articles(contents_keyword, user_query, top_k=5)
    article = ranked_articles[n][1]
    return summarize_article(article) 
    
    