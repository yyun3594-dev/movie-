import os
import requests
from datetime import datetime
import sys
# 强制设置系统编码为utf-8，解决中文文件名报错
sys.stdout.reconfigure(encoding='utf-8')
os.environ["PYTHONIOENCODING"] = "utf-8"

IMG_PATH = "images"
OUT_PATH = "output"

# 【重点】从Github Actions环境秘钥读取，不再手动填密钥！！秘钥名必须是AI_APIKEY
API_KEY = os.getenv("AI_APIKEY")
if not API_KEY:
    print("错误：没有读取到Github密钥AI_APIKEY")
    exit(1)

prompt = """你是小红书电影博主，根据配图写笔记：
1.开头吸睛标题带emoji，正文130字左右，口语种草
2.末尾带上#电影推荐 #高分电影 #影视解说 相关标签
3.严格分成【标题】【正文】【话题】三段"""

if not os.path.exists(IMG_PATH):
    print("images文件夹不存在")
    exit(1)

img_files = [i for i in os.listdir(IMG_PATH) if i.endswith((".png",".jpg",".jpeg",".PNG",".JPG",".JPEG"))]
print("检测到图片列表：", img_files)
if not img_files:
    print("images里没找到图片，程序结束")
    exit(1)

for pic_name in img_files:
    headers = {"Authorization":f"Bearer {API_KEY}", "Content-Type":"application/json"}
    body = {"model":"deepseek-v3","messages":[{"role":"user","content":prompt}]}
    try:
        res = requests.post("https://api.deepseek.com/v1/chat/completions",json=body,headers=headers)
        print("接口原始返回：", res.text)
        res_json = res.json()
        article = res_json["choices"][0]["message"]["content"]
    except Exception as err:
        print("AI接口调用出错：", err)
        exit(1)

    save_name = f"{datetime.now().strftime('%Y%m%d')}_{pic_name[:-4]}.md"
    save_full = os.path.join(OUT_PATH, save_name)
    with open(save_full,"w",encoding="utf-8") as f:
        f.write(article)
    print("\n=====生成的小红书文案=====\n",article)
