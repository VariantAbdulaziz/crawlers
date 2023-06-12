import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
import os
from os.path import exists

PROFILE_DIR = ""
PROFILE = ""

def crawl_detail(driver, detail_url):
    driver.get(detail_url)
    time.sleep(2)
    detail_doc = driver.page_source
    detail_soup = BeautifulSoup(detail_doc, "html.parser")
    title_tag, = detail_soup.find_all("h1", { "class": "h1_product_title"} )
    title, = title_tag.contents

    return [title]


def main():
    NUM_PAGES = 493
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument(fr"user-data-dir={PROFILE_DIR}")
    options.add_argument(f"profile-directory={PROFILE}")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    dump_path = f"{BASE_DIR}/document.csv"
    
    
    first_time = not exists(dump_path)

    with open('document.csv', "w") as fd:
        writer = csv.writer(fd)
        
        if first_time:
            writer.writerow(["Sku", "Stock", "Price$"])
            
        for page in range(1, NUM_PAGES + 1):
            url = f"https://www.aicreplacementparts.com/collections/all-parts?tab=products&page={page}"
            driver.get(url)
            time.sleep(5)

            doc = driver.page_source
            soup = BeautifulSoup(doc, "html.parser")
            for link in soup.find_all("a", { "class": "snize-view-link"} ):
                path = link.get("href")
                detail_url = "https://www.aicreplacementparts.com" + path
                row = crawl_detail(driver, detail_url)
                writer.writerow(row)
            print("finished page:", page)

    driver.quit()

if __name__ == "__main__":
    main()