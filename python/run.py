import time
import os
import autoit
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, WebDriverException
from urllib3.exceptions import NewConnectionError, MaxRetryError
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import logging
from logging import getLogger, StreamHandler, Formatter
from pynput import mouse

# カレントディレクトリを設定
os.chdir(os.path.dirname(__file__))


# -------------------------------------------------------------------------------------------------
# 長い文字列を格納する変数とか
# -------------------------------------------------------------------------------------------------

CSS_PLAYPAUSE_BUTTON = '.ytp-large-play-button'
Addon_Path = os.path.abspath("../addon")
Addon_Install_Button = 'qa-temporary-extension-install-button'

# -------------------------------------------------------------------------------------------------



# -------------------------------------------------------------------------------------------------
# loggerやらブラウザ起動やらの処理（loggerのメッセージレベルの設定もここです）
# -------------------------------------------------------------------------------------------------

# loggerオブジェクトの宣言
logger = getLogger(__name__)

# loggerのログレベル設定(ハンドラに渡すエラーメッセージのレベル)
logger.setLevel(logging.INFO)

# handlerの生成
stream_handler = StreamHandler()

# handlerのログレベル設定(ハンドラが出力するエラーメッセージのレベル)
stream_handler.setLevel(logging.DEBUG)

# ログ出力フォーマット設定 デフォルトは '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# 2021-01-13 16:40:23 [INFO]
# this is format

handler_format = Formatter('%(asctime)s [%(levelname)s]\n%(message)s\n')
stream_handler.setFormatter(handler_format)

# loggerにhandlerをセット
logger.addHandler(stream_handler)
logger.debug("開始")

# geckodriverのパスを指定します（自分の環境に合わせて変更してください）
webdriver_path = 'geckodriver.exe'

# Firefoxのオプションを設定してWebDriverを起動します
options = Options()
# options.add_argument("-profile")
# options.add_argument("../profiles")
# options.add_argument("--headless")  # ヘッドレスモードで実行（GUIを表示しない）
service = Service(executable_path=webdriver_path)
driver = webdriver.Firefox(service=service, options=options)
logger.debug("ブラウザを起動します。")

# 最大の読み込み時間を設定 今回は最大30秒待機できるようにする
wait = WebDriverWait(driver=driver, timeout=30)

# -------------------------------------------------------------------------------------------------



# -------------------------------------------------------------------------------------------------
# 関数
# -------------------------------------------------------------------------------------------------

# アドオンのインストール
def install_addon():
    # Firefoxでアドオン管理ページを開く
    driver.get('about:debugging#/runtime/this-firefox')

    # マウス入力を監視するリスナー (suppress = Trueですべてのマウス入力を無効化)
    Mouselistener = mouse.Listener(suppress = True)
    Mouselistener.start()   # リスナー開始

    wait.until(EC.presence_of_all_elements_located)

    # ローカルフォルダからアドオンを読み込む
    button = WebDriverWait(driver, 15).until(lambda x: x.find_element(by=By.CLASS_NAME, value=Addon_Install_Button))
    button.click()

    time.sleep(1)
    autoit.control_click("[CLASS:#32770]", "Edit2")
    autoit.control_send("[CLASS:#32770]", "Edit2", Addon_Path)
    autoit.control_send("[CLASS:#32770]", "Edit2", "{ENTER}")
    time.sleep(1)
    autoit.control_click("[CLASS:#32770]", "Edit1")
    autoit.control_send("[CLASS:#32770]", "Edit1", "manifest.json")
    autoit.control_click("[CLASS:#32770]", "Button1")
    Mouselistener.stop()    # リスナー終了


def open_url():
    driver.get('https://www.youtube.com/error')
    wait.until(EC.presence_of_all_elements_located)

# -------------------------------------------------------------------------------------------------



# -------------------------------------------------------------------------------------------------
# メイン処理
# -------------------------------------------------------------------------------------------------

# YouTubeにアクセスします
install_addon()
open_url()
logger.debug("YouTubeにアクセスします。")

# 要素が全て検出できるまで待機する
wait.until(EC.presence_of_all_elements_located)

# タイトル取得
title = driver.title
logger.info('再生中... ' + title)

# ループ
while True:
    try:
        time.sleep(1)
        if title != driver.title:
            title = driver.title
            logger.info('再生中... ' + title)
    except KeyboardInterrupt:
        logger.debug("KeyboardInterrupt")
        logger.info("終了します。")
        driver.quit()
        break
    except WebDriverException: # ブラウザを閉じたとき
        logger.debug("WebDriverException")
        logger.info("終了します。")
        driver.quit()
    except ConnectionRefusedError: #以下、ブラウザを閉じたときに発生するエラー
        logger.debug('ConnectionRefusedError')
        raise KeyboardInterrupt
    except NewConnectionError:
        logger.debug('NewConnectionError')
        raise KeyboardInterrupt
    except MaxRetryError:
        logger.debug('MaxRetryError')
        raise KeyboardInterrupt
    except:
        logger.exception("メイン処理内でエラーが発生しました。\n")
        input("動作停止中。Enterで再開します。\n")

# -------------------------------------------------------------------------------------------------