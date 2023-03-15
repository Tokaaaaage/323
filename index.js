// cloudscraperモジュールをインポート
const cloudscraper = require('cloudscraper');
// expressモジュールをインポート
const express = require('express');
const axios = require('axios');

// アプリケーションオブジェクトを作成
const app = express();
// ポート番号を指定
const port = 3000;
// list.txtファイルを読み込むためのfsモジュールをインポート
const fs = require('fs');
// list.txtファイルのパスを指定
const listUrl = new URL('https://github.com/Tokaaaaage/323/raw/main/list.txt');

// クエリパラメーターの文字列を生成する関数
function generateQuery() {
  // ランダムな文字列の長さを指定
  const length = 10;
  // 文字列に含める文字のセット
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  // 空の文字列を用意
  let result = '';
  // 指定した長さ分だけ繰り返す
  for (let i = 0; i < length; i++) {
    // 文字セットからランダムに一文字選ぶ
    let char = chars[Math.floor(Math.random() * chars.length)];
    // 結果の文字列に追加する
    result += char;
  }
  // クエリパラメーターの形式にして返す（?key=value）
  return `?${result}=${result}`;
}
// URLにアクセスする関数（非同期）
async function accessUrl(url) {
  try {
    // cloudscraperでGETリクエストを送る（クエリパラメーターも付加）
    let response = await cloudscraper.get(url + generateQuery());
    // レスポンスの内容とサイズ（バイト数）をコンソールに出力する（URLも含める）
    console.log(`Accessed ${url} and got ${response.length} bytes of data:\n${response}`);
  } catch (error) {
    // エラーが発生した場合はコンソールに出力する（URLも含める）
    console.error(`Failed to access ${url} due to: ${error.message}`);
  }
}
// list.txtファイルからURLを読み込んでアクセスする関数（非同期）
async function accessUrlsFromList() {
  // list.txtファイルを読み込む
  // list.txtファイルを読み込む

  axios.get(listUrl).then((response) => {
    // ファイル内容を改行で分割して配列に格納する
    const urls = response.data.split('\n');
    // 配列の各要素に対して処理する
    for (let url of urls) {
      // URLが空でないかチェックする
      if (url) {
        // URLにアクセスしてレスポンスのステータスコードとデータサイズを取得する
        axios.get(url).then((response) => {
          app.get('/', (req, res) => {
            // レスポンスとしてHello Worldと表示する
            // アクセス中のURLをレスポンスとして送信する
            res.send(`Accessed ${url} with status code ${response.status} and data size ${response.data.length}`);
          });
          console.log(`Accessed ${url} with status code ${response.status} and data size ${response.data.length}`);
        }).catch((error) => {
          res.send(`Failed to access ${url} due to: ${error.message}`);
          console.error(`Failed to access ${url} due to: ${error.message}`);
        });
      }
    }
  }).catch((error) => {
    console.error(`Failed to read ${listUrl} due to: ${error.message}`);
  });
}// アプリケーションにルートパス（/）へのGETリクエストに対するハンドラを設定する

// アプリケーションを指定したポート番号で起動する
app.listen(port, () => {
  // コンソールに起動したことを出力する
  console.log(`App listening at http://localhost:${port}`);
  // list.txtファイルからURLを読み込んでアクセスする関数を呼び出す
  accessUrlsFromList();
  // 1分ごとに同じ関数を繰り返し呼び出す
  setInterval(accessUrlsFromList, 1000);
});
