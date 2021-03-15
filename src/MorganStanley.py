import csv
from datetime import date, timedelta
from .ApiSheetClient import ApiSheetClient
import pandas as pd


class MorganStanleyReader:

    def __init__(self, DDV_Mapping):

        self.EUSIPA_Mapping = {
            "1100 Uncapped Capital Protection": [],
            "1120 Capped Captial Protected": [],
            "1130 Capital Protection with Knock-Out": [],
            "1140 Capital protection with Coupon": [],
            "1199 Miscellaneous Capital Protection": [],
            "1200 Discount Certificates": ["Discount Classic", "Discount Optionsschein Short", 'Discount-Optionsschein'],
            "1220 Reverse Convertibles": ['Aktienanleihe Classic', 'Aktienanleihe Protect'],
            "1230 Barrier Reverse Convertibles": [],
            "1260 Express Certificates": ['Express Classic', 'Express Relax', 'Index Plus', 'Memory Relax Express'],
            "1299 Miscellaneous Yield Enhancement": [],
            "1300 Tracker Certificates": ['Basketzertifikat', 'ZinsFix'],
            "1310 Outperformance Certificates": [],
            "1320 Bonus Certificates": ['Bonus Classic', 'Bonus Cap', 'Bonus Reverse Cap'],
            "1399 Miscellaneous Participation": [],
            "2100 Warrants": ['Optionsschein Classic Long', 'Optionsschein Classic Short', 'Optionsschein'],
            "2199 Miscellaneous Leverage without Knock-Out": [],
            "2200 Knock-Out Warrants": ['X-Turbo', 'X-Turbo Long', 'X-Turbo Short', 'Turbo Short', 'Turbo Long', 'Turbo', 'Endlos Turbo Long', 'Endlos Turbo Short', 'X-Turbo Endlos Long', 'X-Turbo Endlos Short'],
            "2205 Open-end Knock-Out Warrants": ['Turbo Open End', 'X-Turbo Open End'],
            "2210 Mini-Futures": ['Mini-Future', 'X-Mini-Future', 'Mini-Future Long', 'Mini-Future Short'],
            "2299 Miscellaneous Leverage with Knock-Out": [],
            "2300 Constant Leverage Certificate": ['Faktor-Zertifikat'],
            "2399 Miscellaneous Leverage with Knock-Out": [],
            "1340 Twin-Win Certificates": []
        }

        self.client = ApiSheetClient("New Issuance", "Morgan Stanley")

        finaldict = {}
        finaldict["date"] = date.today().strftime('%Y-%m-%d')

        for category in ['Hebelprodukte']:
            resultdict = self.compare(category)
            finaldict[category] = resultdict

        self.client.updateFile(finaldict, DDV_Mapping, self.EUSIPA_Mapping)

    def readData(self, category, date):
        products = []
        with open("/Users/janickspirig/PycharmProjects/IsuanceDataService/sp-handler/data/MorganStanley/{} {}.csv".format(
                category, date), "r",
                  encoding='ISO-8859-1') as f:
            reader = csv.reader(f, delimiter=",")
            next(reader)
            for i, line in enumerate(reader):
                if len(line) > 0:
                    product_id = line[1]
                    try:
                        product_type = line[3]
                    except IndexError:
                        product_type = "NotAllocated"
                    products.append([product_id, product_type])
        return products

    def convertToCSV(self, fname):
        # convert to CSV
        df = pd.read_excel("/Users/janickspirig/PycharmProjects/IsuanceDataService/sp-handler/data/MorganStanley/{}.xlsx".format(fname))
        df.to_csv("/Users/janickspirig/PycharmProjects/IsuanceDataService/sp-handler/data/MorganStanley/{}.csv".format(fname), sep=",")

    def compare(self, category):
        yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        today = date.today().strftime('%Y-%m-%d')

        self.convertToCSV("{} {}".format(category, today))

        oldProducts = self.readData(category, yesterday)
        newProducts = self.readData(category, today)

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