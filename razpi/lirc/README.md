# lirc実験結果

うちのAquosさんを操作することに成功。

## 買い物

IR受信用の仕掛けを作る。[リモコン用IRセンサだけなら2個で100円](http://akizukidenshi.com/catalog/g/gI-04659/)ぐらいで買える。
送信用の[赤外線LEDも5個で100円](http://akizukidenshi.com/catalog/g/gI-03261/)ぐらい。
5Vが強すぎて嫌な人向けには330Ωぐらいの抵抗もあるといいが必須ではない。
あとはメスメスのジャンプワイヤ数本。
正直、これだけだと電車賃や送料のほうが高くてくやしいので、何かのついでに手に入れるのがよい。

## lircインストール、セットアップ

```
root@raspberrypi:~# apt-get install lirc
root@raspberrypi:~# vi /etc/lirc/lirc_options.conf

driver          = default
device          = /dev/lirc0
あとは全部デフォルト

root@raspberrypi:~# vi /boot/config.txt
# IR-Remote controller
dtoverlay=lirc-rpi
dtparam=gpio_in_pin=24
dtparam=gpio_out_pin=25

root@raspberrypi:~# reboot
```


## リモコン学習

リモコン学習手順。irrecordコマンドを使うと.lircd.confファイルが作れる。
これを/etc/lirc/lircd.conf.d/において、lircdを再起動。

```
root@raspberrypi:~# irrecord -f -n
なんかずらずら出る
Please take the time to finish the file as described in
https://sourceforge.net/p/lirc-remotes/wiki/Checklist/ an send it
to  <lirc@bartelmus.de> so it can be made available to others.

Press RETURN to continue.  ＃ Enterを押す

Checking for ambient light  creating too much disturbances.
Please don't press any buttons, just wait a few seconds...

No significant noise (received 0 bytes)

Enter name of remote (only ascii, no spaces) :mytest　　　＃　ここで名前を付ける
Using mytest.lircd.conf as output filename

Now start pressing buttons on your remote control.

It is very important that you press many different buttons randomly
and hold them down for approximately one second. Each button should
generate at least one dot but never more than ten dots of output.
Don't stop pressing buttons until two lines of dots (2x80) have
been generated.

Press RETURN now to start recording.　＃　Enterを押してからリモコンポチポチしまくる
................................................................................

Please enter the name for the next button (press <ENTER> to finish recording)
key_power　　　＃適当にボタン名を付けてボタンを押す

```

### 学習結果確認

irwを立ち上げたあと、センサに向かってリモコンポチポチする。
```
root@raspberrypi:~# irw 
0000000000000001 00 key_power mytest

```

### 命令送信

送信用のLEDをGPIOにつなげて下記コマンドで送信。

```
root@raspberrypi:~# irsend SEND_ONCE mytest key_power
```


### リモコン受信結果で何かをする


irexecを使う。

```
root@raspberrypi:/etc/lirc# vi irexec.lircrc 

begin
    prog   = irexec
    button = key_power
    config = say "テストでーす"
end

root@raspberrypi:~# service irexec restart
```




