import threading
import time
import filetodb
import MySQLdb
import urllib2
import os
import math
from bs4 import BeautifulSoup
import utility



 

def fdb(file,cur):
    lines=utility.get_list_from_file('test.txt')
    for l in lines:
	    cur.execute("""INSERT INTO profile_builder_websiteprofile(website) VALUES (%s)""",(str(l)))
        #db.commit()   

def fetch_url(ids,cur):
    
    i_id=int(ids)
    cur.execute("SELECT website from profile_builder_websiteprofile where id=%s",(i_id))
    url=cur.fetchone()
    return url

def updatedb_notparsed(ids,cur):
    cur.execute("""UPDATE profile_builder_websiteprofile SET website_status=0 where id=(%s)""",(ids))
    #execute("INSERT into lst(url) values('%s')",(url))


def download(start,limit,thread_no):
    db = utility.get_db()

    cur = db.cursor()

    end=start+limit
    print "start="+str(start)+" end="+str(end)+"\n"
    for i in range(start, end):
        url=fetch_url(i,cur)
        
        url=str(url).replace('(u\'','')
        url=str(url).replace('\',)','')
        

        folder=url.replace('http://','')
        folder=folder.replace('/','_')
        folder=folder.replace('.','_')
        try:
            html=utility.get_html_from_url(url)
            print "\n\t"+thread_no+" fetched: "+url+"\n"
            print "\n\t"+thread_no+" value of i="+str(i)+"\n"
            if not os.path.exists(folder):
                print folder
                os.makedirs(folder)
            with open(folder+'/html.txt', "w") as myfile:
                if html!='':
                    myfile.write(str(html))
                cur.execute("UPDATE profile_builder_websiteprofile SET website_status=1 where id=%s",(i))
        except:
            print "Error in this url :"+url 
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
   db=utility.get_db()
   cur=db.cursor()
   cur.execute("SELECT COUNT(*) from profile_builder_websiteprofile")
   p=cur.fetchone()
   print p
   return p[0]

def beg():
    db=utility.get_db()
    cur=db.cursor()
    cur.execute("ALTER table profile_builder_websiteprofile AUTO_INCREMENT = 1")
    fdb('test.txt',cur)
def test_urls():
    db=utility.get_db()
    cur=db.cursor()
    n=count_urls()
    for i in range(1,n):
        print "\n\t"+str(fetch_url(i,cur))+"\n"
    cur.close()

#beg()
no_of_urls=count_urls()
no_of_threads=4
l=float(no_of_urls)/float(no_of_threads)
if(l>math.floor(l)):
    l=l+1
    limit=int(math.floor(l))
if l==0 :
	limit=1
start=0
k=1
test_urls()
try:
    threads = []

    for n in range(1,no_of_threads+1):
        print "\nk="+str(k) +" limit="+str(limit)+"\n"
        thread = threading.Thread(target=download, args=(k,limit,"thread "+str(n)+": "))
        thread.start()

        threads.append(thread)

        k=k+limit
        if n==no_of_threads:
            #limit=no_of_urls%no_of_threads
            print "Last Thread"
        
        print "Waiting..."

    for thread in threads:
        thread.join()

    print "Complete."
    
except IOError:
    print "Error in thread"
while 1:
    pass