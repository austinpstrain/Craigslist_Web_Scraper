# Craigslist web scrapper

This Craigslist web scraping tool is used to grab information from a products based on a search term.


# Requirements and libraries

pip install beautifulsoup
pip install requests

# Usage

Run main.py, Enter 'a' if you want to append to the .csv file or enter 'w' if you want to overwrite .csv file
Search terms are entered from the inputKeywords.txt
main.py will prompt the user for how many pages of products to be searched for corresponding search term
Data will be saved in the craigslist_data.csv
The outputKeywords.txt keeps track of search termse used and how many products were scraped with the corresponding search term