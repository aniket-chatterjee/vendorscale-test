import threading
import time
import MySQLdb
import urllib2
import os
import sys
import math
from bs4 import BeautifulSoup
import utility


def download(Lisst,filename):
    

    
    for link in Lisst:
        
        url=str(link[0]).replace('(u\'','')
        url=str(url).replace('\',)','')
        
        link_url=str(link[1]).replace('\'','')
        folder=str(url).replace('http://','')
        folder=folder.replace('/','_')
        folder=folder.replace('.','_')
        
        try:
            print link_url
            all_links=link_url.split("<br>")
            for al in all_links:
                al='http://'+al
                print al
                i=1
                html=utility.get_html_from_url(al)
                file_path=folder+filename+str(i)+".htm"
                file_i=open(file_path,'w')
                content=file_i.write(html)
                i=i+1
            print link[0]

            #cur.execute("UPDATE profile_builder_websiteprofile SET website_status=1 where id=%s",(i))
        except:
            print "Error in this url :"+url 
    sys.exit()

db = utility.get_db()
cur = db.cursor()
cur.execute("SELECT website,facebook_profile,id FROM profile_builder_websiteprofile where facebook_status=1")
FB=cur.fetchall()

cur.execute("SELECT website,linkedin_profile,id FROM profile_builder_websiteprofile where linkedin_status=1")
LN=cur.fetchall()

cur.execute("SELECT website,twitter_profile,id FROM profile_builder_websiteprofile where twitter_status=1 ")
TW=cur.fetchall()

threads=[]
try:
    thread1 = threading.Thread(target=download, args=(FB,"/facebook"))
    thread2 = threading.Thread(target=download, args=(LN,"/linkedin"))
    thread3 = threading.Thread(target=download, args=(LN,"/twitter"))
    
    thread1.start()
    thread2.start()
    thread3.start()
    threads.append(thread1)
    threads.append(thread2)
    threads.append(thread3)
    print "\n Fetchig pages..."

    for thread in threads:
        thread.join()
except:
    print "thread error"