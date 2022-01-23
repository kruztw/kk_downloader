<div align="center">
    <img src="https://github.com/kruztw/kk_downloader/blob/main/logo.png" height="200">
    <br><br><br><br>
</div>

KK Downloader is a tool to help you download your kkbox music to your computer automatically.


* output
  * store downloaded music
* OK
  * successfully downloaded song list

<br>

# How to run ?

## Install dependency

```shell=
python3 -m pip install --upgrade pip

pip3 install pytube3
pip3 install moviepy
pip3 install bs4

python3 -m pip install --upgrade pytube
python3 -m pip install --upgrade Pillow

sudo apt update
sudo apt install ffmpeg
```


## Export kbl


<div id="mybrand" align="center">
    <img src="https://github.com/kruztw/kk_downloader/blob/main/step1.png" height="300" width="500">
    <br>
    <img src="https://github.com/kruztw/kk_downloader/blob/main/step2.png" height="300" width="500">
</div>


## run kk_downloader

```shell=
python3 kk_downloader.py <kbl>
```


## Issue

### [pytube.exceptions.RegexMatchError: __init__: could not find match for ^\w+\W](https://stackoverflow.com/questions/70776558/pytube-exceptions-regexmatcherror-init-could-not-find-match-for-w-w)

```shell=
pip3 show pytube                  # Location defines here
vim $(Location)\pytube\cipher.py

change Line 30:

before:
var_regex = re.compile(r"^\w+\W")

after:
var_regex = re.compile(r"^\$*\w+\W")
```


## TODO

1. progress bar
2. UI
3. Singer selection (可選擇創作歌手)
4. supporton Windows
