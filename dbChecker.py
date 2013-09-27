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
def company_info(content,url,ids):
    company=utility.extract_company_info_from_html(content,url)
    client_list=company['client_list']
    testimonial_list=company['testimonial_list']
    portfolio_list=company['portfolio_list']
    casestudy_list=company['casestudy_list']
    industry_list=company['industry_list']
    contact_list=company['contact_list']
    linkedin_list=company['linkedin_list']
    facebook_list=company['facebook_list']
    twitter_list=company['twitter_list']
    website_title=company['website_title']
    website_description=company['website_description']
    website_keywords=company['website_keywords']

    website_description=website_description.encode('ascii','ignore')
    website_description=website_description.encode('utf-8','ignore')

    website_title=website_title.encode('ascii','ignore')
    website_title=website_title.encode('utf-8','ignore')
    #for i in facebook_list:
    print facebook_list
    store_metadata(str(website_title),str(website_description),str(website_keywords),ids,url)
    store_website_contact(ids,contact_list)
    store_fb_profile(ids,facebook_list)
    store_twitter_profile(ids,twitter_list)
    store_linkedin_profile(ids,linkedin_list)



def store_fb_profile(ids,facebook_list):
    if facebook_list!='':
        cur.execute("""UPDATE  profile_builder_websiteprofile set facebook_profile="%s",facebook_status=1 where id=%s""",(facebook_list,ids))
def store_twitter_profile(ids,twitter_list):
    if twitter_list!='':
        cur.execute("""UPDATE  profile_builder_websiteprofile set twitter_profile="%s",twitter_status=1 where id=%s""",(twitter_list,ids))
def store_linkedin_profile(ids,linkedin_list):
    #print linkedin_list
    if(linkedin_list!=''):
        cur.execute("""UPDATE  profile_builder_websiteprofile set linkedin_profile="%s", linkedin_status=1 where id=%s""",(linkedin_list,ids))
def store_website_contact(ids,contact_list):
    #pass
    cur.execute("""UPDATE  profile_builder_websiteprofile set website_contact="%s" where id='%s'""",(contact_list,ids))

def store_website_portfolio(ids,portfolio_list):
    #pass
    cur.execute("""UPDATE  profile_builder_websiteprofile set website_portfolio="%s" where id='%s'""",(portfolio_list,ids))

def store_website_testimonial_list(ids,testimonial_list):
    cur.execute("""UPDATE  profile_builder_websiteprofile set website_testimonial="%s" where id='%s'""",(testimonial_list,ids))

def store_website_clients(ids,client_list):
    cur.execute("""UPDATE  profile_builder_websiteprofile set website_clients="%s" where id='%s'""",(client_list,ids))


def store_metadata(title, desc, keywords,ids,url):
    print "\n\tMeta Data Update:"+url
    cur.execute("""UPDATE  profile_builder_websiteprofile set website_title="%s",website_description="%s",website_keywords="%s" where id=%s""",(title, desc, keywords,ids))
    cur.execute("UPDATE  profile_builder_websiteprofile set website_status=2 where id='%s'",(ids))
    print "\n\tupdate Successful \n\n"
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
        company_info(str(content),url,w[1])
        #store_contacts(w[1],w[0])
        
        
    time.sleep(1000)


