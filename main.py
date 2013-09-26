import thread
import time
import filetodb
import MySQLdb
import urllib2
import os
from bs4 import BeautifulSoup
import utility
import unicodedata


 

def fdb(file,cur):
    lines=utility.get_list_from_file('test.txt')
    for l in lines:
	    cur.execute("""INSERT INTO profile_builder_websiteprofile(website) VALUES (%s)""",(str(l)))
        #db.commit()   

def fetch_url(ids,cur):
    print ids
    i_id=int(ids)
    cur.execute("SELECT website from profile_builder_websiteprofile where id=%s",(i_id))
    url=cur.fetchone()
    return url

def updatedb_notparsed(ids,cur):
    cur.execute("""UPDATE profile_builder_websiteprofile SET website_status=0 where id=(%s)""",(ids))
    #execute("INSERT into lst(url) values('%s')",(url))


def download(start,limit):
    db = utility.get_db()

    cur = db.cursor()

    end=start+limit
    print "start="+str(start)+"end="+str(end)
    for i in range(start, end):
        print "i="+str(i)
        url=fetch_url(i,cur)
        
        url=str(url).replace('(u\'','')
        url=str(url).replace('\',)','')
        

        folder=url.replace('http://','')
        folder=folder.replace('/','_')
        folder=folder.replace('.','_')
        html=utility.get_html_from_url(url)
        if not os.path.exists(folder):
            print folder
            os.makedirs(folder)
        with open(folder+'/html.txt', "w") as myfile:
            if html!='':
                myfile.write(html)
        cur.execute("UPDATE profile_builder_websiteprofile SET website_status=%s where id=%s",(1,i))
    cur.close()
        

def alexarating(start,limit):
    db = utility.get_db()

    cur = db.cursor()
    end=start+limit
    print "start="+str(start)+"end="+str(end)
    for i in range(start, end):
        print "i="+str(i)
        url=fetch_url(i,cur)
        
        url=str(url).replace('(u\'','')
        url=str(url).replace('\',)','')
        rating=utility.get_alexa_content(url)
        cur.execute("UPDATE profile_builder_websiteprofile SET alexa=%s where id=%s",(rating,i))
        #utility.get_alexa_rating(ur)
    cur.close()
def count_urls():
   return 4

def beg():
    db=utility.get_db()
    cur=db.cursor()
    cur.execute("ALTER table profile_builder_websiteprofile AUTO_INCREMENT = 1")
    fdb('test.txt',cur)

#beg()
no_of_urls=count_urls()
no_of_threads=5
limit=no_of_urls/no_of_threads
if limit==0 :
	limit=1
start=0
k=0
try:
    for i in range( 1, no_of_threads):
        
        thread.start_new_thread(download, (k,limit))
        thread.start_new_thread(alexarating, (start,limit))
        #alexarating,(start,limit))
        k=k+limit
except IOError:
    print "Error in thread"
while 1:
    pass