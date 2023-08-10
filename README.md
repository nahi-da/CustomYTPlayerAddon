# EmbedYTPlayerAddon

指定した ID のプレイリストをシャッフル再生する埋め込みプレーヤーを、YouTube のエラーページに書き込むアドオンです。

## 使い方

### 注意

- IFrame API をエラーページに書き込む必要があり、これがリモートコードに該当するため、このアドオンは審査に通りませんでした。
- アドオン・python スクリプトの使用は自己責任でお願いします。

### アドオンの使い方

1. [ここ](https://github.com/nahi-da/EmbedYTPlayerAddon/archive/refs/heads/main.zip)からファイルをダウンロードする。
2. ダウンロードしたファイルを解凍し、addon フォルダーの`page-eater.js`を開き、2 行目の`PlaylistId`の内容を、再生したいプレイリストの ID に書き換えておく。
3. Firefox で`about:debugging`を開き、「この Firefox」をクリックする。または、Firefox で`about:debugging#/runtime/this-firefox`を開く。
4. 「一時的なアドオンを読み込む」をクリックする。
5. addon フォルダーのいずれかのファイルを選択する。
6. アドオンが読み込まれたので、`www.youtube.com/error`を開く。
7. エラーページに埋め込みプレーヤーが書き込まれる。
8. ブラウザを終了したらアドオンはアンインストールされるので、次回起動時アドオンを使いたければ、2 からやり直す。

### python スクリプトの使い方

1. （初回のみ）pip でライブラリのインストール。

```
pip install selenium
pip install pyautoit
pip install urllib3
pip install pynput
```

2. （初回のみ）[ここ](https://github.com/mozilla/geckodriver/releases)から、最新の geckodriver をダウンロードし、`geckodriver.exe`を、python フォルダーに入れておく。
3. `run.py`を実行すると、Firefox が起動し、自動でアドオンがインストールされ、エラーページが開く。
4. ブラウザを閉じた後、コンソールがしばらく残るが、終了処理を行っているだけなのでそのままにしておく。（コンソールを閉じると、終了処理が行われず、ブラウザのプロセスが残り続けます。）
