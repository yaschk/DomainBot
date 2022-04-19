import requests


proxies = {
        'http': "http://Selyaschk1999:B5l7AeB@87.251.18.90:45785",
    }

sess = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

ans = sess.get("https://google.com/", proxies=proxies, headers=headers)

#
print(ans.text)
# for step in ans.history:
#     print(step.url)
print(ans.url)