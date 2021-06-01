
from bs4 import BeautifulSoup
from selenium import webdriver


def get_url(search_item, pageNumber):
    url = "https://www.amazon.in/s?k={}&ref=nb_sb_noss".format(search_item)
    url += '&page{}'.format(pageNumber)
    return url


# extract product details
def extract_product_details(item):

    # description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = "https://wwww.amazon.in" + atag.get("href")

    # offer price and original price
    try:
        offer_price_parent = item.find('span', 'a-price')
        offer_price = offer_price_parent.find('span', 'a-offscreen').text
        original_price_parent = item.find('span', 'a-price a-text-price')
        original_price = original_price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return

    result = (description, offer_price, original_price, url)
    return result


# get records from web page
def get_records(records, url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all('div', {'data-component-type': 's-search-result'})
    for item in results:
        record = extract_product_details(item)
        if record:
            records.append(record)


if __name__ == '__main__':

    driver = webdriver.Firefox(executable_path='geckodriver.exe')
    print("scraping amazon...")

    # search item
    search_item = input("Enter name of the product: ")
    # at least 50 record in this list
    records = []

    # to make sure our records contain at least 50 products
    pageNumber = 1
    while len(records) <= 50:
        url = get_url(search_item, pageNumber)
        get_records(records, url)
        print(len(records))
        pageNumber += 1
    index = 1
    for record in records:
        print(index, record[0], record[1], record[2], record[3])
        index += 1
    driver.close()

