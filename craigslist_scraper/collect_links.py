import requests
import re
from bs4 import BeautifulSoup
from scrape_page import *
import time
import math



def collect_search_links(keyword): #Written by Austin
    pages = int(input('\nFor search term "{}" how many pages would you like to search? '.format(keyword.capitalize())))

    base = "https://houston.craigslist.org/search/sss?query="
    productCount = 0
    search_links=[]

    try:
        #Search for keyword on craigslist
        r = requests.get(base+keyword)
        data = r.text
        soup = BeautifulSoup(data, features="lxml")

        #Find the number of pages in result
        resultsQuery = soup.find('span' , attrs={'class' : 'button pagenum'})
        resultsQuery = resultsQuery.text.replace(' ', '').replace('\n', '')
        count = 0
        totalResults = resultsQuery[resultsQuery.find('/')+1:]
        resultsPerPage = resultsQuery[resultsQuery.find('-')+1:resultsQuery.find('/')]
        maxPages = int(totalResults)/int(resultsPerPage)
        maxPages = math.ceil(maxPages)
        print('Total results: ', totalResults)
        print('Results per page: ', resultsPerPage)
        print('Total pages: ', maxPages)

        #Limit pages searched by maxPages
        if(maxPages < pages):
            pages = maxPages

        #Look through each page of results and collect links
        count = 0
        for i in range(pages):
            if int(totalResults) > count:
                productDivs = soup.findAll('li' , attrs={'class' : 'result-row'})
                for product in productDivs:
                    search_links.append(product.find('a')['href'])
                    count += 1
                nextButton = soup.find('a', attrs={'class':'button next'})['href']
                r = requests.get('https://houston.craigslist.org'+nextButton)
                #print('https://houston.craigslist.org'+nextButton)
                data = r.text
                soup = BeautifulSoup(data, features="lxml")
    except:
        search_links = []
        print('No results for search term \"' + keyword + '\"' )
    
    return search_links