import requests
from urllib3.util import Retry
from requests.adapters import HTTPAdapter

import time
import re
from bs4 import BeautifulSoup
from time import localtime

def get_description(soup):
    try:
        description = soup.find('section' , attrs={'id':'postingbody'}).text
        description = description[28:]
    except:
        description = ''
    return description

def get_title(soup):
    try:
        title = soup.find('span', attrs = {'class':'postingtitletext'}).text
    except:
        title = ''
    return title

def get_id(soup):
    try:
        idDIV = soup.find('div', attrs = {'class':'postinginfos'}).text
        startID = idDIV.find('id')
        id = idDIV[startID+4:startID+14]
        id = id.replace(' ','').replace('\n','').strip()
    except:
        id = ''
    return id

def get_brand(soup):
    try:
        attrs = soup.find('p', attrs = {'class':'attrgroup'}).text
        startBrand = attrs.find('manufacturer:')
        if startBrand == -1:
            brand = ''
        else:
            brand = attrs[startBrand+14:]
            endBrand = brand.find('model')
            if endBrand > -1:
                brand = brand[:endBrand-1]
            endBrand = brand.find('size')
            if endBrand > -1:
                brand = brand[:endBrand-1]
        brand = brand.strip().replace('\n', '')
    except:
        brand = ''
    return brand

def get_category(soup):
    try:
        cat = []
        category = soup.find('nav', attrs={'class':'breadcrumbs-container'})
        href = category.find_all('a')
        for i in href:
            i = str(i)
            startI = i.find('>')
            endI = i.find('/a')
            cat.append(i[startI+1:endI-1])
            cat.append(' > ')
        del cat[-1]
    except:
        cat = ''
    return cat

def get_condition(soup):
    try:
        attrs = soup.find('p', attrs = {'class':'attrgroup'}).text
        startCond = attrs.find('condition:')
        if startCond > -1:
            condition = attrs[startCond+11:]
        endCond = condition.find('make')
        if endCond > -1:
            condition = condition[:endCond-2]
        endCond = condition.find('delivery')
        if endCond > -1:
            condition = condition[:endCond-2]
        endCond = condition.find('size')
        if endCond > -1:
            condition = condition[:endCond-2]
        condition = condition.strip()

    except:
        condition = ''
    return condition

def get_location(title):
    try:
        location = title[title.find('(')+1:title.find(')') ]
    except:
        location = ' '
    return location

def get_price(title):
    try:
        startPrice = title.find('$')
        if startPrice > -1:
            price = title[startPrice+1:]
        endPrice = price.find('(')
        if endPrice > -1:
            price = price[:endPrice-1]
        endPrice = price.find(' ')
        if endPrice > -1:
            price = price[:endPrice-1]
    except:
        price = ''
    return price

def get_image(soup):
    try:
        div = soup.find('div', attrs={'class':'slide first visible'})
        image = div.find('img')['src']
    except:
        image = ''
    return image

def get_mpn(soup):
    try:
        attrs = soup.find('p', attrs = {'class':'attrgroup'}).text
        startMPN = attrs.find('model name / number:')
        if startMPN > -1:
            mpn = attrs[startMPN+21:]
        endMPN = mpn.find('make')
        if endMPN > -1:
            mpn = mpn[:endMPN-2]
        endMPN = mpn.find('delivery')
        if endMPN > -1:
            mpn = mpn[:endMPN-2]
        endMPN = mpn.find('size')
        if endMPN > -1:
            mpn = mpn[:endMPN-2]
        mpn = mpn.strip()
    except:
        mpn = ''
    return mpn

def get_postTime(soup):
    try:
        postTime = soup.find('time', attrs={'class':'date timeago'}).text
        postTime = postTime.strip().replace(" ","").replace('\n','')
    except:
        postTime = ''
    return postTime