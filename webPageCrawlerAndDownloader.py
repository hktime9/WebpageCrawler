import requests as rq
from bs4 import BeautifulSoup
import os as os
import urllib.request
import time as time
import sys as sys

def getAllLinks(hostname):
	allLinks= []
	html= getHTML(hostname)
	soup = BeautifulSoup(html, 'html.parser')
	for link in soup.find_all('a'):
		allLinks.append(link.get('href'))

	fullLinks= makeFullLinks(allLinks,hostname)
	return fullLinks

def makeFullLinks(allLinks,url):
	url= getDomain(url)
	size= len(allLinks)
	ret=[]
	for i in range(0,size):
		if (allLinks[i]==None):
			continue
		if "http://" in allLinks[i]:
			ret.append(allLinks[i])
			continue
		if "https://" in allLinks[i]:
			ret.append(allLinks[i])
			continue
		else:
			if(len(allLinks[i])!=0):
				if(allLinks[i][0]=='/'):
					allLinks[i]= url[0:len(url)-1]+allLinks[i]
					ret.append(allLinks[i])
				else:
					allLinks[i]= url+allLinks[i]
					ret.append(allLinks[i])
	return ret

def getHTML(website):
	resp= rq.get(website)
	if(resp.status_code==rq.codes.ok):
		return resp.text
	else:
		return -1

def saveHTML(htmlString):
	string= str(time.process_time())
	filename= string.replace(".","")
	filename= filename+".html"
	with open("./DownloadedPages/"+filename, "w", encoding="utf-8") as f:
		f.write(htmlString)
		f.close
	print("Saved in {}".format(filename))

def getTitle(url):
	html= getHTML(url)
	soup= BeautifulSoup(html, 'html.parser')
	return soup.title.string

def mainRoutine(url):
	html= getHTML(url)
	if(html==-1):
		return 0
	else:
		title= getTitle(url)
		filename= title+".html"
		saveHTML(html)
		return 1

def saveAll(url, visited, flag):
	print("crawling *{}*".format(url))
	if(isValid(url)==0):
		return
	if("login" in url):
		return
	if("///" in url):
		return
	if("/#" in url):
		return
	if(url=="0"):
		return
	if url in visited:
		return
	else:
		status= mainRoutine(url)
		if(status==0):
			return
		else:
			visited.append(url) 
			everyLink= getAllLinks(url)
			if(flag=="internal"):
				host= getDomain(url)
				children= internalLinks(host, everyLink)
			elif(flag=="external"):
				children= everyLink
			else:
				return
			totChildren= len(children)
			for i in range (0, totChildren):
				saveAll(children[i], visited, flag)

def internalLinks(host, links):
	retList= []
	totalLinks= len(links)
	for i in range (0,totalLinks):
		if (host in links[i]):
			retList.append(links[i])
	return retList

def isValid(url):
	newlist= url.split("/")
	size= len(newlist)
	if(newlist[size-1] in newlist[size-2]):
		if(newlist[size-1]==""):
			return 1
		else:
			return 0
	if(newlist[size-1] in newlist[size-3]):
		if(newlist[size-1]==""):
			return 1
		else:
			return 0
	else:
		return 1

def getDomain(url):
	ret= url.split("/")
	string= ret[0]+"//"+ret[2]+"/"
	return string

def crawl(url, flag):
	flag= str(flag)
	if(flag=="-i"):
		flag= "internal"
	elif(flag=="-e"):
		flag= "external"
	else:
		print("I dont know what this flag is")
		time.sleep(1)
		print("Exiting...")
		time.sleep(1)
		return
	print("Beginning to Crawl *{}*".format(url))
	print("Will save webpages to: ./DownloadedPages")
	os.system("mkdir DownloadedPages")
	visited= []
	saveAll(url, visited, flag)
	os.system("cls")
	dir_path = os.path.dirname(os.path.realpath(__file__))+"/DownloadedPages"
	os.chdir(dir_path)
	print("Done!!!!")
	print("Here's Every Page That I Saved:")
	os.system("dir")
	print("Exiting...")

def getCMDArgs():
	cmd= sys.argv
	if(len(cmd)!=3):
		print("URL and Flag needed for execution")
		time.sleep(0.5)
		print("URL in the format: http://www.carameltechstudios.com/")
		print("Flags:")
		print("-i: for crawling internal links only")
		print("-e: for crawling internal and external links")
		time.sleep(0.5)
		print("Re-run with appropriate arguements")
		time.sleep(1)
		print("Exiting...")
		time.sleep(0.5)
		return(-1,-1)
	else:
		return(cmd[1], cmd[2])
		
url, flag= getCMDArgs()
if(url!=-1 and flag!=-1):
	crawl(url, flag)