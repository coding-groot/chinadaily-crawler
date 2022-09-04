import requests
import pandas as pd
import numpy as np
import sqlite3

search=input("검색어를 입력하세요 ")
date_start=input("시작날짜를 입력하세요(Format:YYYY-MM-DD)")
date_finish=input("날짜를 입력하세요(Format:YYYY-MM-DD)")
op=input("duplication removal을 on or off?")
data=[]
url=f'http://newssearch.chinadaily.com.cn/rest/cn/search?publishedDateFrom={date_start}&publishedDateTo={date_finish}&fullMust={search}&sort=dp&duplication={op}&page=1&type=&channel=&source='
response_url=requests.get(url)
r_json = response_url.json()
total_page=r_json['totalPages']
print(f'{total_page} 페이지 남음')
pg = 0
con = 1
for page in range(1,total_page+1):
    print(f'{pg}쪽 완료')
    url=f'http://newssearch.chinadaily.com.cn/rest/cn/search?publishedDateFrom={date_start}&publishedDateTo={date_finish}&fullMust={search}&sort=dp&duplication={op}&page={page}&type=&channel=&source='
    response_url=requests.get(url)
    r_json = response_url.json()
    cont=r_json['content']
    for x in r_json['content']:
        l=[x['id'],x['title'],x['url'],x['plainText'],x['channelName'],x['pubDateStr']]
        data.append(l)
        print(f'{con}번째 기사 완료')
        con += 1
    pg += 1

column=["id","title","url","plainText","channelName","pubDateStr"]
df=pd.DataFrame(data,columns=column)

con = sqlite3.connect("C:/Users/qwe/Desktop/sibeom/newstext.db")
cur = con.cursor()

create_article_table = '''CREATE TABLE IF NOT EXISTS "kpop"(
                                    "id" TEXT,
                                    "title" TEXT,
                                    "url" TEXT,
                                    "plainText" TEXT,
                                    "channelName" TEXT
                                    "pubDateStr" TIMESTAMP)'''

cur.execute(create_article_table)
df.to_sql('kpop',con,index=False,if_exists='append')
