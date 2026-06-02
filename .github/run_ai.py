import os
import requests
from datetime import datetime

API_KEY = os.getenv("API_KEY")
IMG_PATH = "images"
OUT_PATH = "output"
os.makedirs(OUT_PATH, exist_ok=True)

# 小红书文案固定提示词
prompt = """你是小红书电影博主，根据配图写笔记：
1.开头吸睛标题带emoji，正文130字左右，口语种草
2.末尾带上#电影推荐 #高分电影 #电影 相关标签
3.严格分成【标题】【正文】【话题】三段"""

img_files = [i for i in os.listdir(IMG_PATH) if i.endswith(("png","jpg","jpeg"))]
if not img_files:
    exit()

for pic_name in img_files:
    headers = {"Authorization":f"Bearer {API_KEY}", "Content-Type":"application/json"}
    body = {"model":"deepseek-v3","messages":[{"role":"user","content":prompt}]}
    res = requests.post("https://api.deepseek.com/v1/chat/completions",json=body,headers=headers)
    article = res.json()["choices"][0]["message"]["content"]
    save_name = f"{datetime.now().strftime('%Y%m%d')}_{pic_name[:-4]}.md"
    with open(f"{OUT_PATH}/{save_name}","w",encoding="utf-8") as f:
        f.write(article)
