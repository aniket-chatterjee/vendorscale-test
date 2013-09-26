import time
import MySQLdb
import urllib2
import utility
from bs4 import BeautifulSoup


def foldername(url):
    url=str(url).replace('(u\'','')
    url=str(url).replace('\',)','')
        

    folder=url.replace('http://','')
    folder=folder.replace('/','_')
    folder=folder.replace('.','_')
    return folder

def store_metadata(title, desc, keywords,url):
    cur.execute("UPDATE  profile_builder_websiteprofile set website_title='%s' website_description='%s' website_keywords='%' where website='%s'",(title, desc, keywords,url))
    cur.execute("UPDATE  profile_builder_websiteprofile set website_status=2 where website='%s'",(url))
db = utility.get_db()
cur = db.cursor()

while 1:

    cur.execute("SELECT website FROM profile_builder_websiteprofile where website_status=1")
    websites=cur.fetchall()

    for w in websites:
        f=foldername(w)
        url=str(w).replace('(u\'','')
        url=str(url).replace('\',)','')
        soup = BeautifulSoup(f+'html.txt')
        website_metadata = utility.get_website_metadata(soup,url)
        store_metadata(website_metadata.website_description,website_metadata.website_title,website_metadata.website_keywords,w)
        
    time.sleep(100000)


