import time
import MySQLdb
import urllib2
import utility
import os
from bs4 import BeautifulSoup
import codecs

def convert_to_folder(url):
	folder=str(url).replace('http://','')
	folder=folder.replace('/','_')
	folder=folder.replace('.','_')
	return folder
def parse_and_storeFB(FB):
	for links in FB:
		folder=convert_to_folder(links[0])
		f=open(folder+"/facebook1.htm")
		content=f.read()
		if(content!=''):
			company=utility.facebook_parser_public_page(content)
			
			logo = company['logo']
			likes = company['likes']
			name = company['name']
			print "logo:"+logo +" likes:"+likes+" name:"+name
			cur.execute("""UPDATE profile_builder_websiteprofile set company_name="%s",company_logo="%s", fb_likes=%s where id=%s""",(name,str(logo),int(likes),links[1]))
			cur.execute("""UPDATE profile_builder_websiteprofile set facebook_status=2 where id=%s""",(links[1]))

def parse_and_storeLinkedin(LN):
	for links in LN:
		folder=convert_to_folder(links[0])
		f=open(folder+"/linkedin1.htm")
		content=f.read()
		if(content!=''):
			company=utility.linkedin_parser_public_page(content,'')
			company_type = company['company_type']
			head_count=company['head_count']
			website_url = company['website_url']
			industry = company['industry']
			founded =company['founded']
			company_id =company['company_id']
			if(founded==''):
				founded='0'
			logo_url = company['logo_url']
			city=company['city']
			company_description=company['company_description']
			#print "logo_url:"+logo_url +" likes:"+likes+" name:"+name
			cur.execute("""UPDATE profile_builder_websiteprofile set
			 linkedin_description="%s",
			 linkedin_headcount="%s",
			 linkedin_foundedyear=%s,
			 linkedin_city="%s",
			 linkedin_company_id="%s",
			 linkedin_company_type="%s"
			 where id=%s""",
			  (company_description,head_count,int(founded),city,company_id,company_type,links[1]))
			cur.execute("""UPDATE profile_builder_websiteprofile set
				linkedin_status=2 where id=%s""",(links[1]))
def parse_and_storeTwitter():
	pass


db = utility.get_db()
cur = db.cursor()
cur.execute("SELECT website,id FROM profile_builder_websiteprofile where facebook_status=1")
FB=cur.fetchall()

cur.execute("SELECT website,id FROM profile_builder_websiteprofile where linkedin_status=1")
LN=cur.fetchall()

parse_and_storeFB(FB)
parse_and_storeLinkedin(LN)

