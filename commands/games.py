#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = "Marius Pozniakovas"
__email__ = "pozniakovui@gmail.com"
'''module for getting sports game info'''


import urllib
import urllib.request
from bs4 import BeautifulSoup

theurl = 'https://www.flashscore.com/'
theurl = 'https://www.livescore.com/'
thepage = urllib.request.urlopen(theurl)

soup = BeautifulSoup(thepage, 'html.parser')

print (soup.title)

for link in soup.findAll('a'):
     link = link.get('href')
     if 'football' in link or 'basketball' in link:
          print('link')

# for line in soup.findAll('div', {"title":"Click for match detail!"}):
#      print (line)

# for line in soup.findAll('INVALID_DATE_ERROR'):
#      print (line)

# print(soup.find('div', {"class":"sportName basketball"}))

# for row in soup('div', {'class': 'sportName basketball'}):
#     # tds = row('td')
#     # print tds[0].string, tds[1].string
#     print ('hi')