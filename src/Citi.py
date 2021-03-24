import csv
from datetime import date, timedelta
from .ApiSheetClient import ApiSheetClient
import pandas as pd


class CitiBankReader:

    def __init__(self, DDV_Mapping):

        self.EUSIPA_Mapping = {
            "1100 Uncapped Capital Protection": [],
            "1120 Capped Captial Protected": [],
            "1130 Capital Protection with Knock-Out": [],
            "1140 Capital protection with Coupon": [],
            "1199 Miscellaneous Capital Protection": [],
            "1200 Discount Certificates": ['Discount'],
            "1220 Reverse Convertibles": [],
            "1230 Barrier Reverse Convertibles": [],
            "1260 Express Certificates": [],
            "1299 Miscellaneous Yield Enhancement": [],
            "1300 Tracker Certificates": [],
            "1310 Outperformance Certificates": [],
            "1320 Bonus Certificates": [],
            "1399 Miscellaneous Participation": [],
            "2100 Warrants": ['Put', 'Call'],
            "2199 Miscellaneous Leverage without Knock-Out": [],
            "2200 Knock-Out Warrants": ['Turbo Bull','Turbo Bear', 'Open End Turbo Bull', 'Open End Turbo Bear'],
            "2210 Mini-Futures": ['Mini Long','Mini Short'],
            "2299 Miscellaneous Leverage with Knock-Out": [],
            "2300 Constant Leverage Certificate": ['Faktor Long','Faktor Short'],
            "2399 Miscellaneous Leverage with Knock-Out": [],
            "1340 Twin-Win Certificates": []
        }

        self.CATEGORY_Mapping = {
            'Hebelprodukte': ['Turbo Bull','Turbo Bear', 'Put', 'Call', 'Open End Turbo Bull', 'Open End Turbo Bear', 'Mini Long', 'Mini Short','Faktor Long','Faktor Short'],
            'Zertifikate': ['Discount','Bonus','Capped Bonus','Reverse Bonus','Capped Reverse Bonus','Index Tracker','Kapitalschutzzertifikate','Outperformance Zertifikate','Sprint Zertifikate']
        }

        self.client = ApiSheetClient("Issuance Data Collection", "Citi")

        finaldict = {}
        finaldict["date"] = date.today().strftime('%Y-%m-%d')
        for category in ['Zertifikate', 'Hebelprodukte']:
            resultdict = self.compare(category)
            finaldict[category] = resultdict

        self.client.updateFile(finaldict, DDV_Mapping, self.EUSIPA_Mapping)

    def readData(self, category, date):
        products = []
        with open(
                "/Users/janickspirig/PycharmProjects/IsuanceDataService/sp-handler/data/Citi/NewProducts_{}.csv".format(
                        date),
                "r", encoding='ISO-8859-1') as f:
            reader = csv.reader(f, delimiter=",")
            next(reader)
            for i, line in enumerate(reader):
                if len(line) > 0:
                    print(line)
                    if line[8] == date:
                        product_id = line[1]
                        try:
                            product_type = line[4]
                        except IndexError:
                            product_type = "NotAllocated"
                        # check if product type is of this specific category
                        for key, value in self.CATEGORY_Mapping.items():
                            for t in self.CATEGORY_Mapping[key]:

                                if t == product_type:
                                    if key == category:
                                        products.append([product_id, product_type])
        return products

    def convertToCSV(self, date):
        # convert to CSV
        df = pd.read_excel("/Users/janickspirig/PycharmProjects/IsuanceDataService/sp-handler/data/Citi/NewProducts_{}.xls".format(date))
        df.to_csv("/Users/janickspirig/PycharmProjects/IsuanceDataService/sp-handler/data/Citi/NewProducts_{}.csv".format(date), sep=",")

    def compare(self, category):
        today = date.today().strftime('%Y-%m-%d')

        self.convertToCSV(today)

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
