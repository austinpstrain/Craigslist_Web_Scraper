from bs4 import BeautifulSoup
import requests
import schedule
from schedule import every
from collect_links import *
from scrape_page import *
import csv

#Open data file in write mode or append mode
mode = input("Do you want to append (a) data file or write (w) over existing file? (a/w): ")
if mode == 'w':
	check = input("Are you sure you want to overwrite the data file? (y/n): ")
	if check == 'n':
		mode = 'a'
		print ("mode = append")
	else:
		print ("mode = overwrite") 
file = open('craigslist_scraper/craigslist_data.csv', mode)
writer = csv.writer(file, lineterminator = '\n')

#Write headers to cvs file
if mode == 'w':
    writer.writerow(['Items Scraped','Keyword','Product', 'Description' ,'Product ID','Brand','Category','Condition','Location','Price (USD)','Image','URL','MPN'])

#If writing to new data file, overwrite ouputKeywords too.
if mode == 'w': 
	txt = open("craigslist_scraper\ouputKeywords.txt","w")

links = []
listOfLinks = []
inputFile = open('craigslist_scraper\inputKeywords.txt','r+')
words = inputFile.readlines()

#For each key word collect product url's.
txt = open("craigslist_scraper\ouputKeywords.txt",'a+')
keyword = []
keyLengths = []
for line in words:
	line = line.replace('\n','')
	keyword.append(line)
	links = collect_search_links(line)
	for i in links:
		listOfLinks.append(i)
	txt.writelines(line+': '+str(len(links))+'\n') 
	keyLengths.append(len(links))
txt.close()

#Grab all of data for each page
keyCount = 0
keyIndex = 0
for i in listOfLinks:
	r = requests.get(i)
	data = r.text
	soupy = BeautifulSoup(data, features="lxml")
	#go to next keyword when keyCount reaches length of links from that corresponding keyword.
	if keyCount == keyLengths[keyIndex]:
		keyIndex = keyIndex + 1
		keyCount = 0
	searchWord = keyword[keyIndex]
	title = get_title(soupy)
	description = get_description(soupy)
	postID = get_id(soupy)
	brand = get_brand(soupy)
	listCategory = get_category(soupy)
	category = str(listCategory).strip('[]').replace("'","").replace(",","")
	condition = get_condition(soupy)
	location = get_location(title)
	price = get_price(title)
	image = get_image(soupy)
	url = i
	mpn = get_mpn(soupy)
	postTime = get_postTime(soupy)
	keyCount = keyCount + 1

	try:
		print(keyCount,searchWord,title, description ,postID,brand,category,condition,location,price,image,url,mpn)
		print('\n-----------------------------------------------')
		writer.writerow([keyCount,searchWord,title, description ,postID,brand,category,condition,location,price,image,url,mpn])
	except:
		print("DATA OUTPUT FAILED FOR PRODUCT: ", searchWord)

file.close() #close cvs file