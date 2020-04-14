#更丰富的Network跟踪
通过browsermobproxy拿到Chrome的Network中没有的数据并保存到rlog.json中

#使用方法
需要一个cookies.json文件
修改home_page载入cookies.json
修改host找到远程ProxyServer或者自己本地建立一个
修改driver_path找到chrome.exe的位置

#Required
python=3.7
browsermobproxy
selenium
chromedrive.exe