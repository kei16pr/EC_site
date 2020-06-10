#coding: UTF-8
from urllib import request
from bs4 import BeautifulSoup
import requests
import uuid
import pandas as pd
import sys
import csv

#必要な情報
# タイトル、サムネ画像、カテゴリ(タグのこと)、詳細文、リンク
def scraping():
    target_url = "https://jp.pornhub.com/video"
    try:
        html = request.urlopen(target_url)         #requestsを使って、webから取得
    except:
        print("エラーが発生しました")
        sys.exit()
    soup = BeautifulSoup(html, "html.parser")
    # soupにhtmlが格納されている
    Index = soup.find("ul",id="videoCategory")
    # ここからtitle取得
    items = Index.find_all("span", class_="title")
    articles_title = []
    for item in items:
        title = item.text.replace(' ', '').replace('\n', '')
        # if "他サイト引用不可" in title:
        #     # print(title)
        #     continue
        # else:
        articles_title.append(title)
    # ここからrefとtag取得
    href_list=[]
    href_items = Index.select('a.videoPreviewBg')
    tag_list = []
    for href in href_items:
        href_list.append(str("https://jp.pornhub.com")+href.attrs["href"])
        detail_url=str("https://jp.pornhub.com")+href.attrs["href"]
        try:
            detail_html = request.urlopen(detail_url)
        except:
            print("エラーが発生しました")
            sys.exit()
        detail_soup = BeautifulSoup(detail_html, "html.parser")
        tags = detail_soup.select('div.categoriesWrapper a')
        tag_list.append(tag.text for tag in tags if ("+ 追加" and "認証済みユーザー") not in tag.text)
    # ここからthumbnail取得
    img_src_list = [img.get('data-src') for img in Index.select('a.videoPreviewBg img')]
    img_dir_list = []
    for img in img_src_list:
        r = requests.get(img)
        img_dir=str('documents/')+str(uuid.uuid4())+str('.jpeg')
        img_dir_list.append(img_dir)
        with open(str('./media/')+img_dir,'wb') as file:
                file.write(r.content)
    # ここからCSV出力
    with open('./post.csv', 'w') as f:
        writer = csv.writer(f)
        # (["id","title", "thumbnail","tags","detail","ref"])
        for i in range(len(articles_title)):
            writer.writerow([i,articles_title[i],img_dir_list[i], list(tag_list[i]),'',href_list[i]])
    print("正常に終了")

if __name__ == "__main__":
    scraping()
