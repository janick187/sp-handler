import csv
from datetime import date, timedelta
from .ApiSheetClient import ApiSheetClient


class HSBCReader:

    def __init__(self, DDV_Mapping):

        self.EUSIPA_Mapping = {
            "1100 Uncapped Capital Protection": [],
            "1120 Capped Capital Protection": [],
            "1130 Capital Protection with Knock-Out": [],
            "1140 Capital protection with Coupon": [],
            "1199 Miscellaneous Capital Protection": [],
            "1200 Discount Certificates": [],
            "1220 Reverse Convertibles": [],
            "1230 Barrier Reverse Convertibles": [],
            "1240 Capped Outperformance Certificates": [],
            "1260 Express Certificates": [],
            "1299 Miscellaneous Yield Enhancement": [],
            "1300 Tracker Certificates": [],
            "1310 Outperformance Certificates": [],
            "1320 Bonus Certificates": [],
            "1399 Miscellaneous Participation": [],
            "2100 Warrants": [],
            "2199 Miscellaneous Leverage without Knock-Out": [],
            "2200 Knock-Out Warrants": [],
            "2210 Mini-Futures": [],
            "2299 Miscellaneous Leverage with Knock-Out": [],
            "2300 Constant Leverage Certificate": [],
            "2399 Miscellaneous Leverage with Knock-Out": [],
            "1340 Twin-Win Certificates": []
        }

        self.client = ApiSheetClient("New Issuance", "HSBC")

        finaldict = {}
        finaldict["date"] = date.today().strftime('%Y-%m-%d')
        for category in ['Hebelprodukte']:
            resultdict = self.compare(category)
            finaldict[category] = resultdict

        self.client.updateFile(finaldict, DDV_Mapping, self.EUSIPA_Mapping)

    def readData(self, category, date):
        products = []
        with open(
                "/Users/janickspirig/PycharmProjects/IsuanceDataService/sp-handler/data/HSBC/{}_{}.csv".format(
                        category,
                        date),
                "r", encoding='ISO-8859-1') as f:
            reader = csv.reader(f, delimiter=";")
            next(reader)
            for i, line in enumerate(reader):
                if len(line) > 0:
                    if "Fußnoten" in line[0]:
                        break
                    product_id = line[1]
                    try:
                        product_type = line[10]
                    except IndexError:
                        product_type = "NotAllocated"

                    products.append([product_id, product_type])
        return products

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
