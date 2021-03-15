
'''
page = 2

# if there is a text "no reslts found included we do not wantt to proceed!" -> this text has the class "no-results-found__Wrapper-bsj5n8-0"

singlePageUrl = "https://www.gs.de/en/products/investment/bonus-certificates?issuer=gswp&order-by=undefined_asc&page={}&view=simple".format(page)

sel.css('.shout')
'''

import requests
from bs4 import BeautifulSoup


class GoldmanSachsReader:
    def __init__(self):

        categories = ['bonus-certificates']

        self.extractData(categories)


    def getPageContent(self, category, page):
        link = "https://www.gs.de/en/products/investment/{}?issuer=gswp&order-by=undefined_asc&page={}&view=simple".format(category, page)
        site = requests.get(link)
        soup = BeautifulSoup(site.content, 'html.parser')
        all_rows = soup.find_all('a', class_='row')
        products_found = []
        for p in all_rows:
            issuer = p.find('div', class_='issuer-label').text
            if not issuer == "Goldman Sachs":
                continue
            # product category
            category = p.get('href').split("/")[4]
            # ISIN
            id = p.get('href').split("/")[6]
            products_found.append([id, category])

        sublink = soup.findAll("a", {"aria-current": True})[-1].get('href')
        nextpage = int(sublink.split("page=")[1].split("&")[0])

        if not nextpage > page:
            nextpage = False
        else:
            nextpage = True

        return products_found, nextpage


    def writeFile(self, content):
        pass

    def extractData(self, categories):
        page = 1
        nextpage = True

        all_products = []

        for c in categories:

            products_per_category = []

            while nextpage:
                products, nextpage = self.getPageContent(c, page)
                [products_per_category.append(sl) for sl in products]
                print(products_per_category)
                if nextpage:
                    page += 1

            [all_products.append(sl) for sl in products_per_category]
            print(all_products)
            # now we can proceed with the next category / link


        self.writeFile(all_products)


