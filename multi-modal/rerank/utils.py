from sentence_transformers import SentenceTransformer
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import numpy as np


# Load reranker model
model_name = 'BAAI/bge-reranker-v2-m3'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name) 
model.eval()  



def exp_normalize(x):
    """exp_normalize 함수를 거친 scores들의 합은 1""" 
    b = x.max()
    y = np.exp(x - b)
    return y / y.sum() 
        
        