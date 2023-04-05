#! /usr/bin/env python3
import datetime
import os
import random
#import cv2
import cgi ; form = cgi.FieldStorage()
import cgitb ; cgitb.enable()
print("Content-Type: text/html ;charset=utf-8") ; print()

# 日付の取得
today = datetime.datetime.today()
date = str(today.year)+"/"+str(today.month)+"/"+str(today.day)

# HTMLの入力フォームをpythonに受け渡す
LOG_FILE = form.getvalue("file","text/case.txt")
name = form.getvalue("name","").strip()
contents = form.getvalue("contents","").replace("\n","<br>").split()
contents = " ".join(contents)
img_path = form.getvalue("img_path","").strip()
search = form.getvalue("search","").strip()
mode = form.getvalue("mode","and")
img = form.getvalue("img",0)
reverse = form.getvalue("reverse",0)
shuffle = form.getvalue("shuffle",0)

# 画像操作（osモジュールの操作は相対パスだが、pathは/...と絶対パス）
# ローカルの画像をドキュメントルートに保存しなおす
if img_path != "" and name != "" and contents != "":
    img_path = "/users/keimy/desktop/"+img_path
    img_name = "image/img"+today.strftime("%Y%m%d%H%M%S")+".jpg"
    os.rename(img_path, img_name)
    img_path = "/"+img_name
# 画像削除コマンド
if "image/" in search:
    img_name = "image/"+search.split("image/")[1]
    os.remove(img_name)
    search=""

# ログファイルを破壊的に変更する
# ログ上書き：aは追記。これをwにすると全部リセットされてしまうので非推奨
with open(LOG_FILE, mode="a") as f:
    if name != "" and contents != "":
        names = name.split()
        for i in range(len(names)): names[i] = "@"+names[i]
        name = " ".join(names)
        if img_path != "": f.write("【 "+name+" 】@"+date+"<br>"+contents+"<br><img src='"+img_path+"'>"+"\n")
        else: f.write("【 "+name+" 】@"+date+"<br>"+contents+"\n")

# removeコマンド：こちらはwで上書きとする。これをaにすると記載が倍々に増えてしまう。
if "rm" in search:
    try:
        search = int(search.replace("rm","").strip())-1
        if search<0: search=""
        with open(LOG_FILE, mode="r")as f:
            lines = f.readlines(); lines.pop(search)
        with open(LOG_FILE, mode="w")as f:
            f.writelines(lines)
    except: pass
    if type(search)==int: search=""
# ¥¥コマンド：¥を全て削除
if "¥¥" in search:
    with open(LOG_FILE,mode="r")as f: lines=f.readlines()
    with open(LOG_FILE,mode="w")as f:
        ans=[]
        for line in lines: ans.append(line.replace("¥",""))
        f.writelines(ans)
    search=""
# ¥コマンド：こちらはwで上書きとする。これをaにすると記載が倍々に増えてしまう。
if "¥" in search:
    try:
        search = int(search.replace("¥","").strip())-1
        with open(LOG_FILE,mode="r")as f:
            lines=f.readlines(); lines[search]="¥"+lines[search]
        with open(LOG_FILE,mode="w")as f: f.writelines(lines)
    except: pass
    if type(search)==int: search="¥"



# HTML定型文
head = """
    <meta charset="UTF-8">
    <title>Nevernote</title>
    <link href="/stylesheet.css" rel="stylesheet" type="text/css"></link>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    """.format(LOG_FILE)
body = """
    <body name="main" style="background:skyblue ; font-size:15"></body>
       """


# ここから検索アルゴリズム
# index付加したlinesリストを用意
with open(LOG_FILE, mode="r", encoding="utf-8") as f:
    lines=[]; i=1
    for line in f: line = "@"+str("{0:03d}".format(i))+" "+line; lines.append(line); i+=1
lines.reverse()

# 出力用のanssリストを用意
anss=[]

# 空白：直近10表示
if search=="": anss=lines[:10]

# allコマンド：全表示
elif "all" in search: anss=lines

# and検索
elif mode=="and":
        searches = search.split() # 空白区切でsearchesリストに格納
        for line in lines:
            flag = True
            for search in searches:
                if search in line: line = line.replace(search,"<a>"+search+"</a>")
                else: flag = False ; break
            if flag: anss.append(line);

# or検索：imgコマンド対応
elif mode=="or":
        searches = search.split() # 空白区切でsearchesリストに格納
        for line in lines:
            flag = False
            for search in searches:
                if search in line: line = line.replace(search,"<a>"+search+"</a>") ; flag = True
            if flag: anss.append(line);

# img
if img: anss = [ans for ans in anss if "img" in ans]
# shuffle
if shuffle: random.shuffle(anss); anss = anss[:10]
# reverse
elif reverse: anss.reverse()





# 出力
print(head,body)
total=len(lines); hit=len(anss);
print("ヒット数："+str(hit)+" / "+str(total))
cnt = 1
for ans in anss: print("<hr>","<a>"+str(cnt)+"/"+str(hit)+"</a>",ans); cnt += 1
