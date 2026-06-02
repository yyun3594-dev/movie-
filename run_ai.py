import os
import requests
from datetime import datetime

API_KEY = os.getenv("API_KEY")
IMG_PATH = "图片"
OUT_PATH = "输出"
# 提前强制创建文件夹，没有就自动新建，解决找不到目录报错
os.makedirs(IMG_PATH, exist_ok=True)
os.makedirs(OUT_PATH, exist_ok=True)

prompt = """你是小红书电影博主，根据配图写笔记：
1.开头吸睛标题带emoji，正文130字左右，口语种草
2.末尾带上#电影推荐 #高分电影 #影视解说 相关标签
3.严格分成【标题】【正文】【话题】三段"""

# 没有图片直接退出不报错
if not os.path.exists(IMG_PATH):
    exit()
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
# 新增这一行！
print(article)
try:
    res = requests.post("https://api.deepseek.com/v1/chat/completions",json=body,headers=headers)
    article = res.json()["choices"][0]["message"]["content"]
except Exception as e:
    print("接口报错：",e)
    exit()

save_name = f"{datetime.now().strftime('%Y%m%d')}_{pic_name[:-4]}.md"
with open(f"{OUT_PATH}/{save_name}","w",encoding="utf-8") as f:
    f.write(article)
print(article)
