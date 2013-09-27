import requests, MySQLdb, urllib2, csv, time, re
from tidylib import tidy_document
from requests import codes
from urlparse import urlparse
from bs4 import BeautifulSoup
from os.path import splitext, basename
import time, requests

def url_normalize(url,domain):

	if url == "" or domain=="":
		return ''
	if len(url) ==1 and url[0] == '/':
		return url
	if url[-1] == '/':
		url = url[:-1]
	
	index_of_domain = url.find(domain)

	if index_of_domain >=0:
		return url[index_of_domain:]
	
	if index_of_domain == -1:
		return domain +'/' + url
	return ''

def get_html_from_url(url):
	headers = {
    'User-Agent': 'grub-client-1.5.3',
	}

	try:
		r = requests.get(url, headers=headers)		
		print r.status_code
		if r.status_code == requests.codes.ok:
			content, errors = tidy_document(r.content)
			return content
	except Exception, e:
		print e
		return -1

def get_website_metadata(soup,url):
	website_title = ''
	website_description = ''
	website_keywords = ''
	# email = ''
	# email_pattern = '[A-Z0-9._%+-]+@+url'
	try:
		website_title = soup.find(re.compile("^title$", re.I)).text.replace('\n','').strip()
	except Exception, e:
		print e
		website_title = ''

	# try:
	# 	email = soup.find(re.compile(email_pattern, re.I)).text.replace('\n','').strip()
	# except Exception, e:
	# 	print e
	# 	email = ''

	try:
		website_description = soup.find("meta",attrs={'name':re.compile("^description$", re.I)}).get('content')
	except Exception, e:
		print e
		website_description = ''		
	
	try:
		website_keywords = soup.find("meta",attrs={'name':re.compile("^keywords$", re.I)}).get('content')
	except Exception, e:
		print e
		website_keywords = ''

	website_metadata = {'website_title':website_title,'website_description':website_description,'website_keywords':website_keywords}
	return website_metadata

def extract_links_from_html(content,url):
	if content == '':
		return -1
	try:
		page_content, errors = tidy_document(content)
		soup = BeautifulSoup(page_content)
		list_of_links = soup.findAll("a")
		website_metadata = get_website_metadata(soup,url)
		return [list_of_links,website_metadata]
	except Exception, e:
		print e
		return -1


def extract_company_info_from_html(content, url):
	list_of_links,website_metadata = extract_links_from_html(content,url)
	if list_of_links == -1:
		return -1
	client_list = []
	testimonial_list = []
	portfolio_list = []
	casestudy_list = []
	industry_list = []
	contact_list = []
	linkedin_list = []
	facebook_list = []
	twitter_list = []

	CLIENT = ['client','customer','serve']
	TESTIMONIAL = ['testimonial','success']
	PORTFOLIO = ['portfolio']
	CASESTUDY = ['case']
	INDUSTRY = ['industry', 'industries']
	CONTACT = ['contact','write','reach','enquiry','touch','office']
	LINKEDIN = ['linkedin.com']
	FACEBOOK = ['facebook.com']
	TWITTER = ['twitter.com']

	for link in list_of_links:
		text = link.text.lower()
		href = link.get('href')
		if href is None:
			continue
		for client in CLIENT:
			if client in text:
				a = '<a href="http://'+url_normalize(href,url)+'">client</a>'
			 	if a not in client_list:
			 		client_list.append(a)
				break
		
		for testimonial in TESTIMONIAL:
			if testimonial in text:
				b = '<a href="http://'+url_normalize(href,url)+'">testimonial</a>'
			 	if b not in testimonial_list:
			 		testimonial_list.append(b)
				break	

		for portfolio in PORTFOLIO:
			if portfolio in text:
				c = '<a href="http://'+url_normalize(href,url)+'">portfolio</a>'
			 	if c not in portfolio_list:
			 		portfolio_list.append(c)
				break	

		for casestudy in CASESTUDY:
			if casestudy in text:
				d = '<a href="http://'+url_normalize(href,url)+'">casestudy</a>'
			 	if d not in casestudy_list:
			 		casestudy_list.append(d)
				break		

		for industry in INDUSTRY:
			if industry in text:
				e = '<a href="http://'+url_normalize(href,url)+'">industry</a>'
			 	if e not in industry_list:
			 		industry_list.append(e)
				break		

		for contact in CONTACT:
			if contact in text:
				f = '<a href="http://'+url_normalize(href,url)+'">contact</a>'
			 	if f not in contact_list:
			 		contact_list.append(f)
				break
		
		for linkedin in LINKEDIN:
			if linkedin in href:
				g = url_normalize(href,'linkedin.com')
			 	if g not in linkedin_list:
			 		linkedin_list.append(g)
				break		

		for facebook in FACEBOOK:
			if facebook in href:
				# h = '<a href="'+href+'">facebook</a>'
				h = url_normalize(href,'facebook.com')
			 	if h not in facebook_list:
			 		facebook_list.append(h)
				break

		for twitter in TWITTER:
			if twitter in href:
				i = url_normalize(href,'twitter.com')
			 	if i not in twitter_list:
			 		twitter_list.append(i)
				break

	client_list = '<br>'.join(client_list)
	testimonial_list = '<br>'.join(testimonial_list)
	portfolio_list = '<br>'.join(portfolio_list)
	casestudy_list = '<br>'.join(casestudy_list)
	industry_list = '<br>'.join(industry_list)
	contact_list = '<br>'.join(contact_list)
	linkedin_list = '<br>'.join(linkedin_list)
	facebook_list = '<br>'.join(facebook_list)
	twitter_list = '<br>'.join(twitter_list)
	website_object = {
	'client_list':client_list,
	'testimonial_list':testimonial_list,
	'portfolio_list':portfolio_list,
	'casestudy_list':casestudy_list,
	'industry_list':industry_list,
	'contact_list':contact_list,
	'linkedin_list':linkedin_list,
	'facebook_list':facebook_list,
	'twitter_list':twitter_list,
	'website_title':website_metadata.get('website_title'),
	'website_description':website_metadata.get('website_description'),
	'website_keywords':website_metadata.get('website_keywords'),
	}

	return website_object


def linkedin_parser_public_page(page_content, url):
	soup = BeautifulSoup(page_content,"html5lib")
	
	company_name = soup.find("h1").find(text=True).replace('\n','').strip() #get inside content within tag
	
	basic_details = soup.findAll("dd")
	
	if basic_details[0] is not None:
		company_type = ' '.join(basic_details[0].string.split('\n')).strip()
	else:
		company_type = ' '

	if basic_details[1] is not None:
		head_count = basic_details[1].string.replace('employees','').replace('\n','').strip() # content within string
	else:
		head_count = ''
	
	if basic_details[2] is not None:
		website_url = basic_details[2].find("a").string # content within string
	else:
		website_url = ''

	if basic_details[3] is not None:
		industry = basic_details[3].string # content within string
	else:
		industry = ''

	if basic_details[4] is not None:
		founded = basic_details[4].string # content within string
	else:
		founded = ''

	match = re.search(r"company=(.*?)'", page_content, re.M|re.I)
	company_id = ''
	if match:
		company_id = match.group(1)

	address = soup.find("div", { "class" : "adr" })
	logo_url = soup.find("img", { "class" : "logo" })

	if logo_url is not None:
		logo_url = logo_url.get('src')
	else:
		logo_url = ''

	city = soup.find("span", { "class" : "locality" })
	
	if city is None:
		city = ''
	else:
		city = city.text.replace(",","")
	
	company_description = soup.find("div", { "class" : "text-logo" }).text
	company = {"company_name": company_name, "company_description": company_description,"logo_url": logo_url,"company_type":company_type,
	"head_count":head_count,"website_url":website_url,"industry":industry,"address":address,"city":city, "linkedin_page":url,"founded":founded,'company_id':company_id}
	return company

def facebook_parser_public_page(fb_content):
	page_content, errors = tidy_document(fb_content)
	match_logo = re.search(r'(<img class="profilePic(.*?)>)', page_content, re.M|re.I)
	match_name = re.search(r'<span itemprop="name">(.*?)</span>', page_content, re.M|re.I)
	match_followers = re.search(r'<div class="fsm fwn fcg"><div class="fsm fwn fcg">(.*?)</div></div></h2>', page_content, re.M|re.I) # working fine
	logo = ''
	likes = ''
	name = ''
		

	if match_logo:
		source = match_logo.group(0)
		logo = re.search(r'src="(.*?)"', source, re.M|re.I).group(1)

	if match_followers:
		likes = match_followers.group(1).split('\xc2\xb7')[0].replace(' likes','').replace(',','')

	if match_name:
		name = match_name.group(1)
		if name:
			name = name.replace('<span data-hover="tooltip" data-tooltip-position="right" class="_56_f _5dzy _5d-1" id="u_0_6">','')
	return {'name':name.strip(),'logo':logo.strip(),'likes':likes.strip()}


def get_alexa_content(url):
	headers = {
    'User-Agent': 'grub-client-1.5.3',
	}
	try:
		#alexa_data = urllib2.urlopen('http://data.alexa.com/data?cli=10&dat=snbamz&url=%s' % (url)).read()			
		data = urllib2.urlopen('http://data.alexa.com/data?cli=10&dat=snbamz&url=%s' % (url)).read()
		reach_rank = re.findall("REACH[^\d]*(\d+)", data)
		if reach_rank: reach_rank = reach_rank[0]
		else: reach_rank = -1

		popularity_rank = re.findall("POPULARITY[^\d]*(\d+)", data)
		if popularity_rank: popularity_rank = popularity_rank[0]
		else: popularity_rank = -1

		return int(popularity_rank), int(reach_rank)

	except (KeyboardInterrupt, SystemExit):
		return None

def get_alexa_rating(url, file_name):
	try:
		data = urllib2.urlopen('http://data.alexa.com/data?cli=10&dat=snbamz&url=%s' % (url)).read()
		with open('alexa/'+file_name, "a") as myfile: # change file name & file opening mode
			myfile.write(data) # change string which needs to be written
	except Exception, e:
		data = None
		return data

def get_domain(url):
	if url == '':
		return None
	
	url = url.split('/')[0]
	list_of_terms = url.split('.')
	
	if 'wwww' in list_of_terms[0]:
		list_of_terms = list_of_terms[1:]

	if len(list_of_terms) == 2: # .com | .org | .in | .net | .org - eureka.com
		return url

	if len(list_of_terms) == 3: # webdesign.eureka.com | eureka.co.in | eureka.co.uk | .co.za		
		if list_of_terms[-2] == 'co' and len(list_of_terms[-1]) == 2:
			return url
		else:
			return '.'.join(list_of_terms[1:3])
	
	if len(list_of_terms) > 3: # in.answers.yahoo.com
		if list_of_terms[-1] in ['co','com','net']:
			return '.'.join(list_of_terms[-2:])
	else:
		return '[' + url + ']'

def get_list_from_file(file_name):
	list_of_lines = []
	with open(file_name) as infilelist: # change the name of file
			for line in infilelist:
				line = line.replace('\n','').strip() # do whatever with line
				list_of_lines.append(line)
	return list_of_lines

def fetch_rows_from_db():
	cur = get_db().cursor()
	sql_query = "select id, name, website from company_data where (client_link='' and contact_link='') and industry_name = 'Computer Software' order by id desc"
	try:
		cur.execute(sql_query)
	except Exception, e:
		print e
	data = cur.fetchall ()
	with open("ComputerSoftware.html", "a") as myfile:
		myfile.write("<table border='1'>")
		for x in data:
			print 'ID =====> '+ str(x[0])
			print str(x[2])
			check = check_if_client_listed(x[2])
			if check != -1:
				s = '<tr><td>'+str(x[0])+'</td><td>'+str(x[2])+'</td><td>'+convert_list_to_string(check.get("clients_page_url"))+'</td><td>'+convert_list_to_string(check.get("contact_us_page_url"))+'</td></tr>'
			else:
				s=''	
			myfile.write(s)
		myfile.write("</table>")

def run_from_text_file():	
	i = 1
	with open("google_website.txt") as infilelist: # change the name of file
		for line in infilelist:
			line = line.replace('\n','') # do whatever with line
			url = line.replace('_','.').replace('.html','')
			with open("google/home/"+line) as infile:
				extract_company_info_from_html(infile.read(),url)
				print i
				i += 1


def get_db():
	db = MySQLdb.connect(host="localhost", # your host, usually localhost
	user="root", # your username
	passwd="", # your password
	db="vendortest", # database name
	use_unicode=True,
	charset="utf8") # encoding charcode
	return db

def save_company_to_db(url,client_list,testimonial_list,portfolio_list,casestudy_list,industry_list,contact_list,linkedin_list,facebook_list):	
	cur = get_db().cursor()
	sql_query = "INSERT INTO company_contact_info (url,client,testimonial,portfolio,casestudy,industry,contact,linkedin,facebook, twitter) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s,%s)"
	param_values = (url,client_list,testimonial_list,portfolio_list,casestudy_list,industry_list,contact_list,linkedin_list,facebook_list,twitter_list)
	try:
		cur.execute(sql_query, param_values)
	except Exception, e:
		print e

# def test():
# 	# x = get_list_from_file('/home/manishjethani/Desktop/yp.txt')
# 	x = get_list_from_file('Mobile_Application_Development_companies-bangalore.txt')
# 	for i in x:
# 		print i
# 		print get_domain(i)
# 		print '\n'
# 		time.sleep(1)

# test()