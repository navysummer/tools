# -*- coding: UTF-8 -*-
import requests,re,time
url = 'https://www.zabbix.com/documentation/3.4/zh/manual'
base_url = 'https://www.zabbix.com/documentation/3.4/'
seconds = 1
err_url = []
def get_urls():
    res = requests.get(url)
    content = res.text
    pattern = re.compile(r"indexmenu_4848130395ca30b274d8bd.add[(]'(zh/manual.*?)[']", re.S)
    routes = pattern.findall(content)
    urls = [base_url+item for item in routes]
    return urls
 
def download(url):
    download_url = url + "?do=export_pdf"
    print("当前下载url:")
    print(download_url)
    res = requests.get(url)
    if res.status_code == 200 :
        pattern = re.compile(r"<title>(.*?)</title>", re.S)
        title = pattern.findall(res.text)[0].encode("utf-8")
        try:
            filename = title.replace('\\','-').replace('/','-').replace('"','-').replace('*','-').replace('?','-').replace(':','-').replace('<','-').replace('>','-').replace('|','-')
        except Exception:
             title = pattern.findall(res.text)[0]
        filename = title.replace('\\','-').replace('/','-').replace('"','-').replace('*','-').replace('?','-').replace(':','-').replace('<','-').replace('>','-').replace('|','-')
        file = filename + '.pdf'
        res = requests.get(download_url)
        if res.status_code == 200 :
            with open(file,"wb") as f:
                f.write(res.content)
            print('下载成功')
        else:
            print('下载失败')
            err_url.append(download_url)
    else:
        print('获取文件名失败，停止当前下载')
        err_url.append(download_url)
 
 
def downloads(urls):
    for url in urls:
        download(url)
        time.sleep( seconds )
    if len(err_url) :
        print("下载失败的URL:")
        print(err_url)
 
def main():
    print("下载开始")
    urls = get_urls()
    downloads(urls)
    print("下载完成")
 
if __name__ == '__main__':
    main()
