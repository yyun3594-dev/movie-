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

prompt = """p1,2,3是准备发布的电影《xx电影名》图文笔记配图，参考图片内容创作小红书笔记。
你是小红书影视号博主，结合全网热点资讯、真实影评、影片画面情节创作文案：
1.标题≥15个字，搭配贴合内容的emoji；正文活泼年轻化，字数控制150～200字，融合影片近期热点资讯与剧情细节；
2.输出多版本差异化文案，内容拒绝空洞套话、摒弃AI模板化话术，贴近普通观众真实观后感；
3.固定格式：严格分成【标题】【正文】【话题】三段，话题带上相关电影标签、热点标签。"""

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
    # 把图片名字拼进提示词，AI自动根据文件名写文案
    new_msg = f"海报文件名：{pic_name}\n{prompt}"
    body = {"model":"deepseek-v4-pro","messages":[{"role":"user","content":new_msg}]}
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
    print("\n=====最终文案=====\n",article)
