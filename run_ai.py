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

prompt = """p1,p2,p3是准备发布的电影《xx电影名》图文笔记配图，请以此为视觉基础进行小红书笔记创作。
你是一位资深影迷兼小红书影视博主，文风亲切、有独立见解，善于从细节发现共鸣点。请遵循以下要求创作文案：
1.内容核心：
*标题 (≥15字)：提炼影片最打动人心的核心亮点或一个独特的观看理由，避免使用“救命”“谁懂啊”等过载网络叹词。可巧妙使用1-2个emoji点缀。
*正文 (150-200字)：以朋友分享的口吻撰写。必须自然融入影片上映后的真实热点（如票房成绩、特定平台评分、出圈台词/片段、主演相关热议）及具象的剧情/画面细节。表达真实的感受、思考或疑问，而非堆砌华丽空洞的形容词。
*话题：添加3-5个相关话题，包括电影主标签、核心看点标签（如#独特性看点 #特定情感）和热点标签。
2.文案要求：
*输出3个版本，每个版本需围绕不同的、有说服力的“安利点”展开（例如：A版侧重情感/共鸣，B版侧重制作/视听，C版侧重社会议题/思考）。
*语言需“活泼年轻化”，但应通过具体的描述、个人化的体验比喻和扎实的细节来体现，彻底摒弃“绝绝子”“YYDS”“按头安利”等模板化、透支信任感的营销话术。
3.固定格式：严格按以下框架输出，每个版本之间用“---”分隔：
【标题】
【正文】
【话题】"""

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
        res = requests.post("https://api.deepseek.com/v1/chat/completions",json=body,headers=headers,timeout=60)
        print("接口返回原文：",res.text)
        article = res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("接口异常：",e)
        exit(1)

    save_name = f"{datetime.now().strftime('%Y%m%d')}_{pic_name[:-4]}.md"
    with open(os.path.join(OUT_PATH,save_name),"w",encoding="utf-8") as f:
        f.write(article)
    print("\n=====最终文案=====\n",article)
