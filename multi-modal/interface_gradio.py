import os
import base64
from PIL import Image
from config.gpt_api_configs import client
from get_reranked_article import article_summary
import gradio as gr

class ImageProcessor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.img_text = ""

    def encode_image(self):
        with open(self.image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def describe_img(self):
        image = self.encode_image()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an AI assistant that analyzes images and provides detailed descriptions."},
                {"role": "user", "content": [{"type": "text", "text": "이미지 풍경에서 보이는 특징을 묘사해주세요.\n묘사 텍스트에서 포맷에 맞게 키워드를 추출하세요. 키워드 추출: 키워드1, 키워드2, 키워드3"}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}}]}
            ],
            max_tokens=300,
        )
        self.img_text = response.choices[0].message.content
        return self.img_text
    
    def extract_keywords(self):
        marker = '키워드'
        if marker in self.img_text:
            keyword_part = self.img_text.split(marker, 1)[1].strip()
            if keyword_part.startswith("추출:"):
                keyword_part = keyword_part[len("추출:"):].strip()
            keywords = [kw.strip() for kw in keyword_part.split(',')]
            return keywords
        return []

    def process_image_and_query(self, user_query):
        self.describe_img()
        keyword_list = self.extract_keywords()
        contents_keyword = keyword_list[0]
        return article_summary(contents_keyword, user_query, 0)

def launch_interface():
    iface = gr.Interface(
        fn=lambda image_path, user_query: ImageProcessor(image_path).process_image_and_query(user_query),
        inputs=[
            gr.Image(type="filepath", label="이미지 업로드"),
            gr.Textbox(lines=2, placeholder="질문을 입력하세요.", label="질문")
        ],
        outputs="text",
        title="Image-to-Think RAG",
        description="이미지와 질문을 입력하면 관련된 기사를 요약해드립니다."
    )
    iface.launch(share=True)

launch_interface()
