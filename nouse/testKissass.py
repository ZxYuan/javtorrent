# TODO: rewrite plz
# This is for kissass.to

#!/bin/python
# -*- coding: utf-8 -*-
import sys
import urllib2
import urllib
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
url_base = 'http://kickass.to/usearch/'
banngou = 'RCT-554'
out = open('test.txt','w')

def unzip(data):
        import gzip
        import StringIO
        data = StringIO.StringIO(data)
        gz = gzip.GzipFile(fileobj=data)
        data = gz.read()
        gz.close()
        return data

if __name__=="__main__":
	#TODO: check arguments
	banngou = sys.argv[1]
	req = urllib2.Request(url = url_base + banngou, headers = headers)
	html_doc = urllib2.urlopen(req).read() #TODO: check if urlopen fail
	html_doc = unzip(html_doc)
	#print urllib2.urlopen(req).headers.getparam('charset')
	#print html_doc
	out.write(html_doc)
	soup = BeautifulSoup(html_doc, 'lxml')
	#print soup
	download_list = soup.findAll("a",{ "title" : "Download torrent file" })
	seed_num_list = soup.findAll('td',{'class' : 'green center'})
	for seed_num in seed_num_list:
		print seed_num.string
	if len(download_list) == 0:
		print "I can't find the torrent. Plz help urself."
		sys.exit(1)
	for item in download_list:#TODO: find the best torrent and download it
		print 'I find one from ' + item['href']
		dl_url = urllib2.urlopen(item['href'])
		torrent_data = dl_url.read()
		with open(banngou + '.torrent','wb') as torrent_file:
			torrent_file.write(torrent_data)
	print 'Good night!'
	out.close()