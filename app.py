from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbjungle

# HTML 부분
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/memo')
def listing():
    articles = list(db.articles.find({},{'_id':False}))    
    return jsonify({'result':'success', 'articles':articles})

# API 부분
@app.route('/memo', methods=['POST'])
def post_articles():    
    # 1. Client로부터 데이터 받기
    url_receive = request.form['url']
    comment_receive = request.form['comments']

    # 2. 웹 스크래핑
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    data = requests.get(url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']
    url = soup.select_one('meta[property="og:url"]')['content']
    description = soup.select_one('meta[property="og:description"]')['content']

    # 3. result
    article = {'title' : title, 'image':image, 'desc' : description, 'comment' : comment_receive, 'url' : url}

    db.articles.insert_one(article)
    return jsonify({'result':"success", "msg":"POST 연결되었습니다."})

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000, debug=True)


