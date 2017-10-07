﻿# 【FF14】メモ読み上げ用ツール（softalk使用）  

このツールは決まった時間にメモを読み上げる、いわゆるタイマーツールです。  
記憶力の無い人、もしくはゲームスキルが未熟などで悩んでいる方に使ってもらえればと思います。  

スクリプトは以下の2つです。  
・make_wav.py (もしくはdist/make_wav.exe)  
・play_wav.py (もしくはdist/play_wav.exe)  

## make_wav.py  
メモから音声を作成するツールです。  

1. 注意事項  
** こちらは[softalk](https://www35.atwiki.jp/softalk/pages/15.html)という読み上げ・録音ツールがないと使用できません。  
** 上記URLからダウンロードしたのち、zipの中にあるsoftalkフォルダを同じフォルダにおいてください。  
** （pythonから相対パスでsoftalk/softalk.exeを起動します。）  

2. 事前準備  
  * こちらのツールは使う前にメモを作成する必要があります。  
  * メモの記載方法は以下の通りです。    
  `[時間],[文章]`  
  * [時間]にはメモを読み上げる時間を記載可能です。記載方法は秒数をそのまま描くか、何分:何秒という書き方も可能です。  
  * [文章]には読み上げる内容を記載します。  
    + （例１：「30,テスト1」と記載した場合、30秒経った時に“テスト1”と読み上げられます。）  
    + （例２：「1:30,テスト2」と記載した場合、90秒経った時に“テスト2”と読み上げられます。）  
  * 作者がオメガ４層で使用しているメモの例も入っていますので、参考になればと思います。（example/omega4.txt）  

3. ツール使用方法  
  * コマンドプロンプトからの使い方は以下の通りです。  
  `$ python make_wav.py [事前に作成したメモの名前] [作成する音声(zip)ファイルの名前]`  
  * もしくは  
  `$ dist\make_wav.exe [事前に作成したメモの名前] [作成する音声(zip)ファイルの名前]`  

## play_wav.py  
作成した音声を再生するツールです。  

1. ツール使用方法  
使い方は以下の通りです。  
`$ python play_wav.py [作成した音声(zip)ファイルの名前]`  
もしくは  
`$ dist\play_wav.exe [作成した音声(zip)ファイルの名前]`  

2. 実際の使用方法  
実行すると、“エンターキーを押したらタイマーを開始します”とウィンドウに表示されます。  
ウィンドウをアクティブにした上でエンターキーを押すと、その時を0秒として読み上げが開始します。  

デスクトップかどこかにショートカットを作ることをお勧めします。  
ショートカットを作成した後に、右クリックからプロパティを開き、リンク先のplay_wav.(py/exe)の後に" [作成した音声(zip)ファイルの名前]"を追記してください。  
コマンドプロンプトのウィンドウが表示されますが、レイアウトタブから位置・サイズ設定も可能です。  




