# coding: utf-8
import zipfile
import re
import os
import sys
import shutil
import datetime

softalk_path = "softalk\\softalkw.exe"
option = " /T:0 /V:100 /S:120 /A:120"

def wav_out(word, out):
    if word is not None:
        word_opt = " /W:" + word
    else:
        word_opt = " /W:てすと"
    if out is not None:
        out_opt = " /R:" + out
    else:
        out_opt = ""
    print('"' + softalk_path + option + out_opt + word_opt + '"')
    os.system('"' + softalk_path + option + out_opt + word_opt + '"')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("{} [in_list] [out_zip]".format(sys.argv[0]))
        sys.exit()

    wav_out("wavファイルを作成します", None)
    
    times = []
    words = []
    txtfile = sys.argv[1]
    out_zip = sys.argv[2]
    
    # in_listの内容(time, txt)をリスト化
    with open(txtfile, "r") as f:
        readlines = f.readlines()
    for line in readlines:
        splittxt = re.sub("\r|\n", "", line)
        if splittxt == "":
            continue
        splittxt = splittxt.split(",")
        timetxt = splittxt[0].split(":")
        floattime = 0
        for i, txt in enumerate(reversed(timetxt)):
            floattime += float(txt) * pow(60, i)
        times.append(floattime)
        words.append(splittxt[1])
    
    # wavファイルを一時保存するtmpディレクトリを作成
    tmp_dir = os.path.dirname(os.path.abspath(__file__)) + "\\tmp\\"
    if os.path.exists(tmp_dir) is False:
        os.makedirs(tmp_dir)
    
    # in_listの内容のwavファイルを順次tmpフォルダに作成
    wavs = []
    for i, w in enumerate(words):
        filename = "{0:04d}.wav".format(i)
        wav_out(w, tmp_dir + filename)
        wavs.append(filename)
    
    # timeとwavファイルの対応などを記したlist.txtを作成
    with open(tmp_dir + "list.txt", "w", encoding="utf-8") as f:
        for i, (t, wv, wd) in enumerate(zip(times, wavs, words)):
            f.write("{},{},{},{}\n".format(i, t, wv, wd))
    
    # list.txtとすべてのwavファイルをzip化
    zipFile = zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED)
    zipFile.write(tmp_dir + "list.txt", "list.txt")
    for w in wavs:
        zipFile.write(tmp_dir + w, w)
    zipFile.close()

    # tmpフォルダを削除
    shutil.rmtree(tmp_dir)

    wav_out("wavファイルの作成が終了しました", None)
