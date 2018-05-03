# Raspberry PI 3にseleinumを入れた時のメモ

結構はまったので忘れないようにメモする。

## インストール

バリバリとパッケージをインストール

```
root@raspberrypi:~# sudo apt-get install chromium-browser -y
root@raspberrypi:~# sudo apt-get install fonts-ipafont-gothic fonts-ipafont-mincho -y
root@raspberrypi:~# sudo apt-get install dirmngr -y
root@raspberrypi:~# gpg --keyserver pgp.mit.edu --recv-keys 9D6D8F6BC857C906
root@raspberrypi:~# gpg --armor --export 9D6D8F6BC857C906 | apt-key add -
root@raspberrypi:~# echo "deb http://security.debian.org/debian-security stretch/updates main" > /etc/apt/sources.list.d/security.debian.list
root@raspberrypi:~# apt-get update
root@raspberrypi:~# apt-get install chromium-driver -y                                                                                                                                                                          
root@raspberrypi:~# chromedriver --version
root@raspberrypi:~# pip install -U pip
root@raspberrypi:~# pip install selenium
```

## 動作確認

下記のコードを試してみる。うまくいけばtest.pngというファイルができてるはず。
```
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
  
CHROME_BIN = "/usr/bin/chromium-browser"
CHROME_DRIVER = '/usr/bin/chromedriver'
   
options = Options()
options.binary_location = CHROME_BIN
options.add_argument('--headless')
options.add_argument('--window-size=1280,1080')
    
driver = webdriver.Chrome(CHROME_DRIVER, chrome_options=options)
     
driver.get("https://www.google.co.jp")
driver.save_screenshot("./test.png")
driver.quit()
```


## はまりどころ

* Firefox使おうとしたらいろいろとダメだった。
* Googleのchrome driver公式ページにおいてあるドライバはarmじゃ動かない
* dirmngrってなんだよ・・・
* chromium-driverを入れても実行ファイル名はchromedriver
