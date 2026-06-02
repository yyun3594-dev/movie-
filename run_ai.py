import os
import requests
from datetime import datetime
import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
os.environ["PYTHONIOENCODING"] = "utf-8"

IMG_PATH = "images"
OUT_PATH = "output"

# 直接在这里粘贴你的sk-密钥！！
API_KEY = "sk-2ac15ee0b4384fcdbac13d04291ad360"

prompt = """你是小红书电影博主，根据配图写笔记：
1.开头吸睛标题带emoji，正文130字左右，口语种草
2.末尾带上#电影推荐 #高分电影 #影视解说 相关标签
3.严格分成【标题】【正文】【话题】三段"""

if not os.path.exists(IMG_PATH):
    print("images文件夹不存在")
    exit(1)

img_files = [i for i in os.listdir(IMG_PATH) if i.endswith((".png",".jpg",".jpeg",".PNG",".JPG",".JPEG"))]
print("✅检测图片：", img_files)
if not img_files:
    print("无图片")
    exit(1)

for pic_name in img_files:
    headers = {"Authorization":f"Bearer {API_KEY}", "Content-Type":"application/json"}
    body = {"model":"deepseek-v3","messages":[{"role":"user","content":prompt}]}
    try:
        res = requests.post("https://api.deepseek.com/v1/chat/completions",json=body,headers=headers,timeout=30)
        print("接口返回原文：",res.text)
        article = res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("接口异常：",e)
        exit(1)

    save_name = f"{datetime.now().strftime('%Y%m%d')}_{pic_name[:-4]}.md"
    with open(os.path.join(OUT_PATH,save_name),"w",encoding="utf-8") as f:
        f.write(article)
    print("\n========最终文案========\n",article)
