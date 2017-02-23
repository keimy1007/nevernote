#! /usr/bin/env python3
import cgi ; form = cgi.FieldStorage()
import cgitb ; cgitb.enable()
print("Content-Type: text/html") ; print()


# 読み込むファイル名
LOG_FILE = "tecom.txt"

# 日付の取得
import datetime
today = datetime.datetime.today()
date = str(today.month)+"/"+str(today.day)

# HTMLの内容
head = """
    <h2><font color="blue"><i>Never Note</i></font></h2>
    <input type="button" value="テコム" onclick="window.open('https://www2.tecomgroup.jp/tm/m_menu.jsp')">
    <input type="button" value="国家試験検索" onclick="window.open('/search.html')">
    <input type="button" value="雑記帳" onclick="window.open('http://tsunepi.hatenablog.com/')"></p>
    """

body = """
    <body bgcolor="lightblue">
    <form action="main.py" method="post">
        科目：<input type="text" name="name" size=20 value="循環１８：先天性心疾患まとめ">
        画像PATH：<input type="text" name="img_path" size=10>
        画像URL：<input type="text" name="img_url" size=10>
        日付：<input type="text" name="date" size=5 value="{0}"></p>
        <textarea name="contents" rows=7 cols=100 ></textarea></p>
        検索：<input type="text" name="search" size=20 value="">
        and <input type="text" name="and_search" size=20>
        <input type="submit" value="実行">
    </form>

    """.format(date)

# HTMLの入力フォームをpythonに受け渡す
name = form.getvalue("name","")
contents = form.getvalue("contents","").replace("\n","<br>").split()
contents = " ".join(contents)
img_url = form.getvalue("img_url","")
img_path = form.getvalue("img_path")
date = form.getvalue("date","")
search = form.getvalue("search","")
and_search = form.getvalue("and_search","")

# ローカルの画像をドキュメントルートに保存しなおす
if img_path != None and name != "" and contents != "":
    import os
    img_path = img_path.strip()
    if "image/" in img_path: os.remove(img_path) # 一応、image/からのパスで削除できる。
    else:
        img_name = "image/img"+today.strftime("%Y%m%d%H%M%S")+".jpg"
        os.rename(img_path, img_name)
        img_path = "/"+img_name # img srcに渡すときは/image...じゃないといけない。

# ログを上書き（aだと上書き、wだと全消し）
with open(LOG_FILE, mode="a") as f:
    if name != "" and contents != "":
        if img_url != "": f.write("<hr>【 "+name+" 】"+date+"<br>"+contents+"<br><img src='"+img_url+"'>"+"\n")
        elif img_path != None: f.write("<hr>【 "+name+" 】"+date+"<br>"+contents+"<br><img src='"+img_path+"'>"+"\n")
        else: f.write("<hr>【 "+name+" 】"+date+"<br>"+contents+"\n")

# HTMLを出力
print(head,body)
with open(LOG_FILE, mode="r") as f:
    # １行ずつlogリストに格納
    log = []
    for line in f: log.append(line)
    # reverseコマンドあれば古い順に表示。
    if "reverse" in search: pass
    else: log.reverse()
    # 初期状態：空白かreverseなら、上５件表示
    if search=="" or search=="reverse":
        log = log[0:10]
        for line in log: print(line)
    # 全表示：allコマンド
    elif "all" in search:
        for line in log: print(line)
    # and検索：検索ワードを赤くする。img検索で画像表示。
    elif and_search != "":
        for line in log:
            if (search in line) and (and_search in line):
                if search=="img": pass
                else: line = line.replace(search,"<font color='red'>"+search+"</font>")
                if and_search=="img": pass
                else: line = line.replace(and_search,"<font color='red'>"+and_search+"</font>")
                print(line)
    # or検索は空白区切：検索ワードを赤くする。img検索で画像表示。
    else:
        searches = search.split() # 空白区切でsearchesリストとして格納
        for line in log:
            for i in searches:
                if i in line:
                    if i=="img": pass
                    else: line = line.replace(i,"<font color='red'>"+i+"</font>")
                    print(line)


