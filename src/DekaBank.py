import requests
import csv
from datetime import date, timedelta
from .ApiSheetClient import ApiSheetClient

class DekaBankReader():

    def __init__(self, DDV_Mapping):

        self.EUSIPA_Mapping = {
            "1100 Uncapped Capital Protection": [],
            "1120 Capped Capital Protected": [],
            "1130 Capital Protection with Knock-Out": [],
            "1140 Capital Protection with Coupon": [],
            "1199 Miscellaneous Capital Protection": [],
            "1200 Discount Certificates": [],
            "1220 Reverse Convertibles": ['Aktienanleihe','Aktienanleihe Plus','DuoRendite Aktienanleihe', 'DuoRendite Aktienanleihe Pro'],
            "1230 Barrier Reverse Convertibles": [],
            "1260 Express Certificates": ['Express-Aktienanleihe Plus','Best Express-Zertifikat Relax','Best-In Express-Zertifikat Relax','Express-Zertifikat Memory',
                                    'Express-Zertifikat Memory mit Airbag','Express-Zertifikat Pro','Express-Zertifikat Relax','Express-Zertifikat Relax mit Airbag',
                                    'Express-Zertifikat VarioZins Spezial'],
            "1299 Miscellaneous Yield Enhancement": [],
            "1300 Tracker Certificates": [],
            "1310 Outperformance Certificates": [],
            "1320 Bonus Certificates": ['Bonus-Zertifikat Pro','Reverse-Bonus-Zertifikat mit Cap'],
            "1330 Outperformance Bonus Certificates": [],
            "1340 Twin-Win Certificates": [],
            "1399 Miscellaneous Participation": [],
            "2100 Warrants": [],
            "2110 Spread Warrants": [],
            "2199 Miscellaneous Leverage without Knock-Out": [],
            "2200 Knock-Out Warrants": [],
            "2210 Mini-Futures": [],
            "2299 Miscellaneous Leverage with Knock-Out": [],
            "2300 Constant Leverage Certificate": [],
            "2399 Miscellaneous Constant Leverage Products": []
        }


        # get the current product data over their API
        products = self.getData()
        #and now gernerate the file which is needed as comparison for tomorrow ofc
        self.generateFile(products)

        self.client = ApiSheetClient("New Issuance", "DekaBank")

        finaldict = {}
        finaldict["date"] = date.today().strftime('%Y-%m-%d')

        for category in ['Zertifikate']:
            resultdict = self.compare(category)
            finaldict[category] = resultdict

        self.client.updateFile(finaldict, DDV_Mapping, self.EUSIPA_Mapping)

    def getData(self):

        products = []

        lastPage= False
        index = 1

        while not lastPage:
            body = {
                "filterAuswahl": {
                    "schnellsuche": "",
                    "produktstatus": {
                        "auswahl": [
                            {
                                "s": "NewEmmissions"
                            }
                        ]
                    },
                    "nachhaltigkeit": {
                        "auswahl": [
                            {
                                "s": ""
                            }
                        ]
                    },
                    "produkttyp": {
                        "auswahl": [
                            {
                                "typ": {
                                    "s": ""
                                }
                            }
                        ]
                    },
                    "dbdVerwahrfaehig": {
                        "auswahl": [
                            {
                                "s": ""
                            }
                        ]
                    },
                    "basiswert": {
                        "auswahl": [
                            {
                                "s": ""
                            }
                        ]
                    },
                    "anzahlBasiswerte": {
                        "auswahl": [
                            {
                                "s": ""
                            }
                        ]
                    },
                    "restlaufzeit": {
                        "auswahl": [
                            {
                                "s": "All"
                            }
                        ]
                    },
                    "rueckzahlungstermin": {
                        "von": "",
                        "bis": ""
                    },
                    "as_sfid": "AAAAAAWil9uBVJa5Cjyu2mI5ElkOTYGJahum1VLov6Fsm3BCQueWe-KPn6ZKxjiZUNSwfCAoeblwf3nb8yR0gRAYZfF1YM5DpwiS3X8x68KSYqwDAhJg_0HCL8mjXgdo1uELNew=",
                    "as_fid": "7644aaa3bf42320ccd863246ab6a48f2b0a712fe",
                    "seite": {
                        "index": index,
                        "groesse": 50
                    },
                    "sortierung": {
                        "nach": "",
                        "absteigend": "false"
                    }
                }
            }

            url = "https://www.deka.de/zertifikate/zertifikatsuche?action=sucheZertifikate&zertifikateZipSuche=true&service=zertifikatesucheController"
            data = requests.post(url, json=body).json()

            for p in data['eintraege']:
                id = p['eintrag']['isin']['w']
                type = p['eintrag']['produkttyp']['w']
                products.append([id, type])

            print(len(products))

            if data['anzahlGesamt'] == len(products):
                break
            else:
                index += 1

        return products

    def generateFile(self, products):
        today = date.today().strftime("%Y-%m-%d")
        with open('/Users/janickspirig/PycharmProjects/IsuanceDataService/sp-handler/data/DekaBank/Zertifikate-{}.csv'.format(today), mode='w') as csv_file:
            fieldnames = ['id','type']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for p in products:
                writer.writerow({'id': p[0], 'type': p[1]})

    def readData(self, date, category):
        products = []
        with open(
                "/Users/janickspirig/PycharmProjects/IsuanceDataService/sp-handler/data/DekaBank/{}-{}.csv".format(
                        category, date),
                "r", encoding='ISO-8859-1') as f:
            reader = csv.reader(f, delimiter=",")
            next(reader)
            for i, line in enumerate(reader):
                if len(line) > 0:
                    print(line)
                    product_id = line[0]
                    try:
                        product_type = line[1]
                    except IndexError:
                        product_type = "NotAllocated"
                    products.append([product_id, product_type])
        return products

    def compare(self, category):
        yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        today = date.today().strftime('%Y-%m-%d')
        oldProducts = self.readData(yesterday, category)
        newProducts = self.readData(today, category)
        count_dict = {}
        for x in newProducts:
            if not any(x[0] in sl for sl in oldProducts):
                if not x[1] in count_dict.keys():
                    count_dict[x[1]] = {}
                    count_dict[x[1]]['amount'] = 1
                    count_dict[x[1]]['ISINs'] = [x[0]]
                    # product type and then we have the number, so lets do product type as key and then another nested dict with number and examples --> and here at examples we put in some random IDs
                else:
                    count_dict[x[1]]['amount'] = count_dict[x[1]]['amount'] + 1
                    count_dict[x[1]]['ISINs'].append(x[0])
        return count_dict