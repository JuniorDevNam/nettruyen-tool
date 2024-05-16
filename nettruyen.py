import requests
from bs4 import BeautifulSoup
from os.path import join
from os import makedirs
import sys
import random
import time

user_agent_list = [
   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
   "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
   "Mozilla/5.0 (iPad; CPU OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/104.0.5112.99 Mobile/15E148 Safari/604.1",
   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.3",
   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0"
]
reffer_list=[
   'https://nettruyenco.vn/',
   'https://nettruyencc.com/'
]
thisfoldir = sys.path[0]
download_dir = join(thisfoldir,"nettruyen_download_results")
makedirs(download_dir,exist_ok=True)


def onechapter(web, headers):
    res = requests.get(web,headers=headers)
    html_content = res.text
    soup = BeautifulSoup(html_content, 'html.parser')
    #debug
    #print(soup)
    img_links = []
    for x in soup.find_all("div", class_="page-chapter"):
        for y in x.find_all("img"):
            img_links.append(y.get("data-src"))
    #debug
    #print(img_links)
    parts = web.split("/")
    folder = join(download_dir,parts[-3],parts[-2])
    makedirs(folder, exist_ok=True)
    for index, link in enumerate(img_links):
        print(link)
        file = join(folder,f"image_{index}.jpg")
        response = requests.get(link, headers=headers)
        with open(file, "wb") as f:
            f.write(response.content)
    time.sleep(1)
    print("Xong.")

def multichapters(web, headers):
    res = requests.get(web,headers=headers)
    html_content = res.text
    soup = BeautifulSoup(html_content, 'html.parser')
    #debug
    #with open(debug_html, 'w') as f:
    #    f.write(soup)
    # Find all <a> tags within the specified <div>
    links = []
    for item in soup.find_all("div", class_="list-chapter"):
        for link in item.find_all("a"):
            links.append(link.get("href"))
    links.reverse()
    #debug
    #print(links)
    for x in range(1,len(links)+1):
        #debug
        #print(x)
        onechapter(links[x],headers)


web = str(input("Nhập đường link của truyện: "))
print("**!** Tool còn nhiều hạn chế, và mình sẽ luôn cố gắng cập nhật để bắt kịp với trang web.")
referer = f'https://{web.split("/")[2]}/'
if referer in reffer_list:
    print(referer,"OK.")
    print("Running...")
else:
    print("Phát hiện tên miền mới chưa có trong danh sách hỗ trợ:",referer)
    print("Tool vẫn sẽ chạy nhưng có thể gặp lỗi.")
    print("Nếu được bạn có thể liên hệ với mình để cập nhật tool.")
    time.sleep(5)
    print("Running...")
headers = {
   'Connection': 'keep-alive',
   'Cache-Control': 'max-age=0',
   'Upgrade-Insecure-Requests': '1',
   'User-Agent': random.choice(user_agent_list),
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
   'Accept-Encoding': 'gzip, deflate',
   'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
   #'referer': random.choice(reffer_list)
   'referer': referer
    }

if "chapter" in web:
    onechapter(web, headers)
elif "chuong" in web:
    onechapter(web, headers)
else:
    print("Có vẻ như đây là đường link của cả một truyện?")
    print("Nếu vậy, chờ một lát, công cụ sẽ tải toàn bộ tất cả các chương đang có của truyện")
    multichapters(web, headers)