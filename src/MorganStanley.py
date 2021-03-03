import csv
from datetime import date, timedelta
from .ApiSheetClient import ApiSheetClient
import pandas as pd


class MorganStanleyReader:

    def __init__(self, eusipa):

        self.DDV_Mapping = {
            "Kapitalschutzzertifikate": [],
            "Strukturierte Anleihen": [],
            "Bonitätsabhnhögige Schuldverschreibungen": [],
            "Aktienanleihen": [],
            "Discount-Zertifikate": [],
            "Express-Zertifikate": [],
            "Bonus-Zertifikate": [],
            "Index/-Partizipations-Zertifikate": [],
            "Outperofrmance-/Sprint-Zertifikate": [],
            "Optionsscheine": ['Optionsschein', 'Discount-Optionsschein'],
            "Faktor-Zertifikate": ['Faktor-Zertifikat'],
            "Knock-Out Zertifikate": ['Mini-Future', 'X-Mini-Future', 'Turbo Open End', 'Turbo', 'X-Turbo Open End', 'X-Turbos']
        }

        self.client = ApiSheetClient("New Issuance", "Morgan Stanley")

        finaldict = {}
        finaldict["date"] = date.today().strftime('%Y-%m-%d')

        for category in ['Hebelprodukte']:
            resultdict = self.compare(category)
            finaldict[category] = resultdict

        self.client.updateFile(finaldict, self.DDV_Mapping, eusipa)

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
                    count_dict[x[1]] = 1
                else:
                    count_dict[x[1]] = count_dict[x[1]] + 1
        return count_dict