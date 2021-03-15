import csv
from datetime import date, timedelta
from .ApiSheetClient import ApiSheetClient
import requests

class SGReader:

    def __init__(self, DDV_Mapping):

        self.EUSIPA_Mapping = {
            "1100 Uncapped Capital Protection": ["Kapitalschutz-Zertifikate"],
            "1120 Capped Capital Protection": [],
            "1130 Capital Protection with Knock-Out": [],
            "1140 Capital protection with Coupon": [],
            "1199 Miscellaneous Capital Protection": [],
            "1200 Discount Certificates": ["Discount-Zertifikate", "Classic Discount-Zertifikat"],
            "1220 Reverse Convertibles": ["Classic Aktienanleihen", "Classic Aktienanleihen", "Aktienanleihen Plus", "Aktienanleihen PlusPro", "Aktienanleihen Protect"],
            "1230 Barrier Reverse Convertibles": [],
            "1240 Capped Outperformance Certificates": ["Sprint-Zertifikat"],
            "1260 Express Certificates": ["Memory Express-Zertifikat", "Duo Memory Express-Zertifikat", "Multi Express-Zertifikat", "Multi Memory Express-Zertifikat", "Stufenexpress-Zertifikat", "Fixkupon Express-Zertifikat", "Duo Fixkupon Express-Zertifikat"],
            "1299 Miscellaneous Yield Enhancement": [],
            "1300 Tracker Certificates": ["Index-Zertifiakte", "Short Index-Zertifikate"],
            "1310 Outperformance Certificates": ["Outperformance-Zertifikat"],
            "1320 Bonus Certificates": ["Classic Bonus-Zertifiakt", "Bonus-Zertifiakte Pro", "Capped Bonus-Zertifiakt", "Capped Bonus-Zertifiakt Pro","Reverse Capped Bonus-Zertifikat"],
            "1399 Miscellaneous Participation": [],
            "2100 Warrants": ["Standard-Optionsscheine", "Discount-Optionsscheine", "Inline-Optionsscheine", "StayLow-Optionsscheine", "StayHigh-Optionsscheine", "Turbo-Optionsscheine", "Classic Turbo-Optionsscheine", "Unlimited Turbo-Optionsscheine", "Smart Turbo-Optionsscheine", "BEST Turbo-Optionsscheine", "X-BEST Turbo Optionsscheine", "Faktor-Optionsscheine"],
            "2199 Miscellaneous Leverage without Knock-Out": [],
            "2200 Knock-Out Warrants": [],
            "2210 Mini-Futures": [],
            "2299 Miscellaneous Leverage with Knock-Out": [],
            "2300 Constant Leverage Certificate": [],
            "2399 Miscellaneous Leverage with Knock-Out": [],
            "1340 Twin-Win Certificates": []
        }

        self.Mapping = {
            "Zertifikate": {
                "Aktienanleihen": {
                    53: {
                        59: "Classic Aktienanleihen",
                        59: "Aktienanleihen Plus",
                        61: "Aktienanleihen PlusPro",
                        62: "Aktienanleihen Protect"
                    },
                },
                "Bonus-Zertifikate": {
                    16: {
                        17: "Classic Bonus-Zertifiakt",
                        18: "Bonus-Zertifiakte Pro",
                        19: "Capped Bonus-Zertifiakt",
                        204: "Capped Bonus-Zertifiakt Pro",
                        86: "Reverse Capped Bonus-Zertifikat"
                    }
                },
                "Kapitalschutz-Zertifikate": {
                    15: {}
                },
                "Discount-Zertifikate": {
                    20: {
                        21: "Classic Discount-Zertifikat"
                    }
                },
                "Express-Zertifikate": {
                    56: {
                        44043: "Memory Express-Zertifikat",
                        44037: "Duo Memory Express-Zertifikat",
                        44044: "Multi Express-Zertifikat",
                        44045: "Multi Memory Express-Zertifikat",
                        44046: "Stufenexpress-Zertifikat",
                        44038: "Fixkupon Express-Zertifikat",
                        44086: "Duo Fixkupon Express-Zertifikat"
                    }
                },
                "Outperformance-Zertifikat": {
                    30: {}
                },
                "Sprint-Zertifikat": {
                    37: {}
                },
                "Alpha-Zertifikat": {
                    93: {}
                },
                "Index-Zertifiakte": {
                    27: {
                        44093: "Short Index-Zertifikate"
                    }
                },
            },
            "Hebelprodukte": {
                "Optionsscheine": {
                    1: {
                        2: "Standard-Optionsscheine",
                        12: "Discount-Optionsscheine",
                        8: "Inline-Optionsscheine",
                        44059: "StayLow-Optionsscheine",
                        44056: "StayHigh-Optionsscheine"
                    }
                },
                "Turbo-Optionsscheine": {
                    42: {
                        43: "Classic Turbo-Optionsscheine",
                        45: "Unlimited Turbo-Optionsscheine",
                        49: "Smart Turbo-Optionsscheine",
                        47: "BEST Turbo-Optionsscheine",
                        7145: "X-BEST Turbo Optionsscheine"
                    }
                },
                "Faktor-Optionsscheine": {
                    228: {}
                }
            }
        }

        self.client = ApiSheetClient("New Issuance", "SG")

        finaldict = {}
        finaldict["date"] = date.today().strftime('%Y-%m-%d')

        for category in ['Zertifikate', 'Hebelprodukte']:
            resultdict = self.readData(category)
            finaldict[category] = resultdict

        self.client.updateFile(finaldict, DDV_Mapping, self.EUSIPA_Mapping, Volumen=False, ExchangeData=True)


    def createResultDict(self, newProducts):

        count_dict = {}
        for x in newProducts:
            if not x[1] in count_dict.keys():
                count_dict[x[1]] = {}
                count_dict[x[1]]['amount'] = 1
                count_dict[x[1]]['exchange'] = 0
                count_dict[x[1]]['not exchange'] = 0

                if x[2]:
                    count_dict[x[1]]['exchange'] += 1
                else:
                    count_dict[x[1]]['not exchange'] += 1

                count_dict[x[1]]['ISINs'] = [x[0]]
                # product type and then we have the number, so lets do product type as key and then another nested dict with number and examples --> and here at examples we put in some random IDs
            else:
                count_dict[x[1]]['amount'] = count_dict[x[1]]['amount'] + 1
                count_dict[x[1]]['ISINs'].append(x[0])

                if x[2]:
                    count_dict[x[1]]['exchange'] = count_dict[x[1]]['exchange'] + 1
                else:
                    count_dict[x[1]]['not exchange'] = count_dict[x[1]]['not exchange'] + 1

        return count_dict

    def getProducts(self, id, p_type):
        all_products = []
        today = date.today().strftime('%Y-%m-%d')
        pageNum = 1
        nextPage = True
        while nextPage:
            url = "https://www.sg-zertifikate.de/EmcWebApi/api/ProductSearch/Search?PageSize=1000&PageNum={}&ProductClassificationId={}&IssueDateFrom={}".format(str(pageNum), str(id), today)
            print(url)
            response = requests.get(url)
            if response.status_code == 200:
                json = response.json()
                total = json['TotalCount']
                products = json['Products']
                for p in products:
                    isin = p["Isin"]
                    if p['IsSecondaryMarket']:
                        exchange = True
                    else:
                        exchange = False
                    all_products.append([isin, p_type, exchange])
                if not total > (1000*pageNum):
                    nextPage = False
                else:
                    pageNum += 1

        return all_products

    def readData(self, category):

        all_products = []

        for parent_name in self.Mapping[category]:
            parent_id = list(self.Mapping[category][parent_name].keys())[0]
            parent_products = self.getProducts(parent_id, parent_name)

            for sub_id, sub_name in self.Mapping[category][parent_name][parent_id].items():
                sub_products = self.getProducts(sub_id, sub_name)
                if len(sub_products) > 0:
                    [all_products.append(x) for x in sub_products]
                    # remove sub_product from parent product
                    for item in sub_products:
                        for item2 in parent_products:
                            if item[0] == item2[0]:
                                parent_products.remove(item2)

            [all_products.append(x) for x in parent_products]

        return self.createResultDict(all_products)

    '''
    def compare(self, category):
        today = date.today().strftime('%Y-%m-%d')
        newProducts = self.readData(category, today)
        count_dict = {}
        for x in newProducts:
            if not x[1] in count_dict.keys():
                count_dict[x[1]] = {}
                count_dict[x[1]]['amount'] = 1
                count_dict[x[1]]['ISINs'] = [x[0]]
                # product type and then we have the number, so lets do product type as key and then another nested dict with number and examples --> and here at examples we put in some random IDs
            else:
                count_dict[x[1]]['amount'] = count_dict[x[1]]['amount'] + 1
                count_dict[x[1]]['ISINs'].append(x[0])
        return count_dict
'''