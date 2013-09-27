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
        
        link_url='http://'+str(link[1]).replace('\'','')
        folder=str(url).replace('http://','')
        folder=folder.replace('/','_')
        folder=folder.replace('.','_')
        file_path=folder+filename
        try:
            print link_url
            html=utility.get_html_from_url(link_url)
            #print str(html)
            file_i=open(file_path,'w')
            content=file_i.write(html)
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
threads=[]
try:
    thread1 = threading.Thread(target=download, args=(FB,"/facebook.htm"))
    thread2 = threading.Thread(target=download, args=(LN,"/linkedin.htm"))
    thread1.start()
    thread2.start()
    threads.append(thread1)
    threads.append(thread2)
    print "\n Fetchig pages..."

    for thread in threads:
        thread.join()
except:
    print "thread error"