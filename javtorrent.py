# TODO: Fix bug1

#!/bin/python
# -*- coding: utf-8 -*-
import sys
import urllib2
import urllib
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

url_base = ['http://sukebei.nyaa.se/?term=', 'http://kickass.to/usearch/']
banngou = 'ABP-119'

# unzip gzip html doc
def unzip(data):
        import gzip
        import StringIO
        data = StringIO.StringIO(data)
        gz = gzip.GzipFile(fileobj=data)
        data = gz.read()
        gz.close()
        return data

# return a valid soup object based on the input url
def makeSoup(url):
	req = urllib2.Request(url = url, headers = headers)
	try:
		response = urllib2.urlopen(req) #TODO: check if urlopen fail
	except urllib2.HTTPError, e:
		if e.code == 404:
			return False
		else:
			print 'guagua'
	html_doc = response.read()
	if response.info().get('Content-Encoding') == 'gzip':
		print 'zip'
		html_doc = unzip(html_doc)
	soup = BeautifulSoup(html_doc, 'lxml')
	return soup

# check arguments
def getBanngou(args):
	if len(args) != 2:
		print 'Error: wrong arguments.'
		sys.exit(1)
	return args[1]

# search for the required torrent
def searchTorrent():
	for item in url_base:
		soup = makeSoup(item + banngou)
		if not soup:
			continue
		if 'nyaa' in item:
			download_list = soup.findAll("a",{ "title" : "Download" })
			if download_list:
				print '...find ' + banngou + ' ' + download_list[0]['href']
				return download_list[0]['href']
		elif 'kickass' in item:
			download_list = soup.findAll("a",{ "title" : "Download torrent file" })
			if download_list:
				print '...find ' + banngou + ' ' + download_list[0]['href']
				return download_list[0]['href']
		else:
			#TODO: Add other torrent-dl website
			continue
	print 'Cannot find ' + banngou + '. Google it by yourself.' 
	sys.exit(1)

# download torrent to local file
# bug1: torrents downloaded from kickass in this way(Both urllib & urllib2) seem invalid
def dl2local(dl_url):
	urllib.urlretrieve(dl_url, banngou + '.torrent')
	if 0:
		torrent_data = urllib2.urlopen(dl_url).read()
		with open(banngou + '.torrent','wb') as torrent_file:
			torrent_file.write(torrent_data)
	print banngou + '.torrent successfully downloaded'

if __name__=="__main__":
	banngou = getBanngou(sys.argv) #
	dl_url = searchTorrent() #
	dl2local(dl_url) #