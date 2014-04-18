# TODO: Fix the ugly code format
# I like strong zero from suntory, yeah now it's true that im a little drunk...
# maybe it seems better to refer to different torrent website...but strong zero is really exciting

# -*- coding: utf-8 -*-
import sys
import urllib2
import urllib
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

url_base = 'http://sukebei.nyaa.se/?term='
banngou = 'RCT-554'

if __name__=="__main__":
	#TODO: check arguments
	banngou = sys.argv[1]
	req = urllib2.Request(url = url_base + banngou, headers = headers)
	html_doc = urllib2.urlopen(req).read() #TODO: check if urlopen fail
	soup = BeautifulSoup(html_doc, 'lxml')
	download_list = soup.findAll("td",{ "class" : "tlistdownload" })
	if len(download_list) == 0:
		print "I can't find the torrent. Plz help urself."
		sys.exit(1)
	for item in download_list:#TODO: find the best torrent and download it
		print 'I find one from ' + item.a['href']
		dl_url = urllib2.urlopen(item.a['href'])
		torrent_data = dl_url.read()
		with open(banngou + '.torrent','wb') as torrent_file:
			torrent_file.write(torrent_data)
	print 'Good night!'