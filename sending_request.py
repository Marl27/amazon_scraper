import requests
from bs4 import BeautifulSoup

# sorted values on sponsored products being written to file
def getting_product_info(data):
    sorted_on_sponsored = sorted(data, key=lambda i: i[-1])
    for element in sorted_on_sponsored:
        info_writer = str(element[0]) + ', ' + str(element[1]) + ', ' + str(element[2]) + ', ' + str(element[3])
        with open("products_info.csv", "a") as f:
            f.write(info_writer+ '\n')


def main_loop():
    list_of_tuples = []
    is_sponsored = False
    for s in soup.find_all("div",  attrs={"class":"a-section a-spacing-base"}):
        getting_href = s.find("a", attrs={"class":'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

        if s.find("span", attrs={"class":'a-color-secondary'}) is not None:
            if s.find("span", attrs={"class":'a-color-secondary'}).string == 'Sponsored':
                is_sponsored = True
            else:
                is_sponsored = False

        individual_product_page = requests.get(BASE_URL+getting_href.get('href'), headers=HEADERS)
        individual_product_soup = BeautifulSoup(individual_product_page.content, "lxml")
        title = individual_product_soup.find("span", attrs={"id":'productTitle'}).string.strip()
        try:
            price = individual_product_soup.find("span", attrs={'id':'sns-base-price'})
        except AttributeError:
            price = ""
        try:
            ratings = individual_product_soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string
        except AttributeError:
            ratings = ""

        #geting price using slicing, .get(ATTR) didn't work for some reason
        if price != "":
            price = str(price)[38:44]

        title = title.replace(',','%2C') # Encoding comma character to UTF-8

        data = (title, price, ratings, is_sponsored)
        list_of_tuples.append(data)

    getting_product_info(list_of_tuples)


# HEADER taken from https://developers.whatismybrowser.com/useragents/parse/237874491chrome-windows-blink
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})


#URL = "https://www.amazon.co.uk/s?k=cat+food&ref=nb_sb_noss"
BASE_URL = "https://www.amazon.co.uk"
BASE_URL_VARIABLE = "/s?k="

BASE_URL_ARGUMENT = "cat+food"

web_page = requests.get(BASE_URL + BASE_URL_VARIABLE + BASE_URL_ARGUMENT, headers=HEADERS)
soup = BeautifulSoup(web_page.content, "lxml")
main_loop()
