# coding: utf-8
import wave
import pyaudio
import time
import zipfile
import threading
import datetime
import sys
import re

# 再生用のコールバック関数を定義
def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)

def playAudio(wf):
    p = pyaudio.PyAudio() # PyAudioのインスタンスを生成 (1)
    
    # Streamを生成(3)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)
    
    # Streamをつかって再生開始 (4)
    stream.start_stream()
    
    # 再生中はひとまず待っておきます (5)
    while stream.is_active():
        time.sleep(0.1)
    
    # 再生が終わると、ストリームを停止・解放 (6)
    stream.stop_stream()
    stream.close()
    wf.close()
    
    # close PyAudio (7)
    p.terminate()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("{} [zipfile]".format(sys.argv[0]))
        sys.exit()

    # zipファイルをOpenし、中のinfolistを取り出し
    zipFile = zipfile.ZipFile(sys.argv[1], 'r')
    infolist = zipFile.infolist()
    infodict = {info.filename:info for info in infolist}
    
    # zipファイル内にlist.txtがなければエラー
    # list.txtがあればinfolistからlist.txtの情報を抜き出し
    if "list.txt" not in infodict:
        print("Invalid zipFile filelist: {}".format(infodict))
    else:
        listfile = zipFile.open(infodict["list.txt"]) 
        readlines = listfile.read().decode('utf-8').split("\r\n")
        del infodict["list.txt"]
    
    # まずはすべてのwavファイルをオープンし、wait時間と対応づけておく
    wfs = []
    for line in readlines:
        splittxt = re.sub("\r|\n", "", line)
        splittxt = splittxt.split(",")
        if len(splittxt) < 4:
            continue

        wait = float(splittxt[1])
        key = splittxt[2]
        txt = splittxt[3]
        if key not in infodict:
            print("Invalid key: {}".format(key))
            continue

        wf = wave.open(zipFile.open(infodict[key]), "rb")
        wfs.append((wait, wf, txt))
    sorted(wfs)
    
    # 入力があるまでwait
    print("エンターキーを押したらタイマーを開始します...")
    input()

    # タイマー開始, wait時間になったら対応するwavファイルをスレッドで再生
    start = datetime.datetime.now()
    idx = 0
    ths = []
    while True:
        now = datetime.datetime.now()
        td = now - start
        print(td, end="\r")

        if td.total_seconds() >= wfs[idx][0]:
            wait, wf, txt = wfs[idx]
            print("{0}, {1}".format(datetime.timedelta(seconds=wait),
                txt if len(txt) > 10 else txt + "          "))
            ths.append(threading.Thread(target=playAudio, args=(wf,)))
            ths[-1].start()
            idx += 1

        time.sleep(0.2)
        if idx >= len(wfs):
            break
    
    # 最後にすべてのスレッドがクローズするまで待つ
    for t in ths:
        t.join()
