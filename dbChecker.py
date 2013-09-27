import time
import MySQLdb
import urllib2
import utility
import os
from bs4 import BeautifulSoup
import codecs

def foldername(url):
    
    #url=url[0].replace('(u\'','')
    
    #url=url[0].replace('\',)',' ')
    #url=url[0].encode('utf-8')
   
    folder=url[0].replace('http://','')
    folder=folder.replace('/','_')
    folder=folder.replace('.','_')
    
    return folder

def store_metadata(title, desc, keywords,ids):
    cur.execute("""UPDATE  profile_builder_websiteprofile set website_title="%s",website_description="%s",website_keywords="%s" where id=%s""",(title, desc, keywords,ids))
    cur.execute("UPDATE  profile_builder_websiteprofile set website_status=2 where id='%s'",(ids))
db = utility.get_db()
cur = db.cursor()

while 1:

    cur.execute("SELECT website,id FROM profile_builder_websiteprofile where website_status=1")
    websites=cur.fetchall()

    for w in websites:
        f=foldername(w)
             
        file_path=f+'/html.txt'
        #file_path=file_path.replace('\', 2L)','')
        file_i=open(file_path,'r')
        content=file_i.read()
        
        url=str(w[0]).replace('(u\'','')
        url=str(url).replace('\', 1L)','')
        print url
        soup = BeautifulSoup(str(content))
        website_metadata = utility.get_website_metadata(soup,url)

        description=website_metadata['website_description']
        title=website_metadata['website_title']
        keywords=website_metadata['website_keywords']
        
        description=description.encode('ascii','ignore')
        description=description.encode('utf-8','ignore')

        title=title.encode('ascii','ignore')
        title=title.encode('utf-8','ignore')
        #title=title.replace('\'\'','')
        #title=title.replace('\'','')
        print str(title)
        print description
        store_metadata(str(title),str(description),str(keywords),w[1])
        
    time.sleep(100000)


