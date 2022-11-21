# Part 1

import csv
from selenium import webdriver

import requests
from bs4 import BeautifulSoup

def get_url():               
    # *** Generate a url from search term ***
    template = 'https://www.amazon.in/s?k=bags&page={}&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'

    #add term query to url
    return template 


def extract_record(item):
    # ****Extract and return data from a single record*****
    # * description and url
        atag = item.h2.a
        description = atag.text.strip()
        url = "https://www.amazon.in" + atag.get('href')
        try:
    #   price
            price_parent = item.find('span', "a-price")
            price = price_parent.find('span', "a-offscreen").text
        except AttributeError:
            return
        
        try:
        #rank and rating
            rating = item.i.text
            review_count = item.find('span' , {'class': 'a-row a-size-small', 'dir': 'auto'}).text
        except AttributeError:
            rating = ''
            review_count = ''
            

        result = (description, price, rating, review_count, url)
        return result

def main():

    driver = webdriver.Chrome()
    url = get_url()
    records = []

    for page in range(1, 21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type':'s-search-result'})
        
        for item in results:
                record = extract_record(item)
                if record:
                    records.append(record)


    driver.close()
    # save data to csv file
    with open('results.csv', 'w', newline='' , encoding ='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Rating' , 'ReviewCount', 'Url'])
        writer.writerows(records)

main()