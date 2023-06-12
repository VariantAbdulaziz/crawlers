import csv
from bs4 import BeautifulSoup
import requests


def extract(soup):
    boxes = soup.find_all("div", { "class" : "sccds_member_info_box" })
    book = []
    for box in boxes:
        name, = box.find("h3")
        temp = [name]
        for p in box.find_all("p"):
            key, = p.find("span", { "class" : "sccds_member_field_title" })
            val, = p.find("span", { "class" : "sccds_member_field_c" })
            temp.append(val)
        book.append(temp)
    return book

def main():
    NUM_PAGES = 2 # 139
    with open('document.csv', "w") as fd:
        writer = csv.writer(fd)
            
        for page in range(1, NUM_PAGES + 1):
            url = f"https://sccds.org/member-directory/page/{page}/?seed=481"
            doc = requests.get(url)
            soup = BeautifulSoup(doc.content, "html.parser")

            writer.writerows(extract(soup))
            print("finished with page:", page)

if __name__ == "__main__":
    main()