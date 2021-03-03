import csv
from datetime import date, timedelta
from .ApiSheetClient import ApiSheetClient
import pandas as pd
from itertools import chain


class BNPReader:

    def __init__(self, eusipa):

        self.DDV_Mapping = {
            "Kapitalschutzzertifikate": [],
            "Strukturierte Anleihen": ['Strukturierte Anleihe'],
            "Bonitätsabhnhögige Schuldverschreibungen": [],
            "Aktienanleihen": ['Aktienanleihe Classic', 'Aktienanleihe Protect', 'Aktienanleihe Protect Last Minute'],
            "Discount-Zertifikate": ['Discount'],
            "Express-Zertifikate": ['Best Express Zertifikat', 'Express Zertifikat', 'Klassik Express Zertifikat', 'Memory Express Zertifikat'],
            "Bonus-Zertifikate": ['Bonus', 'Bonus PRO', 'Capped Bonus', 'Capped Bonus PRO', 'Capped Reverse Bonus', 'Capped Reverse Bonus PRO', 'Last Minute Bonus', 'Last Minute Capped Bonus'],
            "Index/-Partizipations-Zertifikate": ['Indexanleihe Protect', 'Partizipationszertifikat'],
            "Outperofrmance-/Sprint-Zertifikate": [],
            "Optionsscheine": ['Put', 'Call', 'Discount-Optionsschein'],
            "Faktor-Zertifikate": ['Faktor Long', 'Faktor Short'],
            "Knock-Out Zertifikate": [],
            "TBC": ['ETC', 'Festzinsanleihe', 'Open End Zertifikat', 'Reverse Bonus', 'Reverse Bonus PRO']
        }

        self.client = ApiSheetClient("New Issuance", "BNP")

        finaldict = {}
        finaldict["date"] = date.today().strftime('%Y-%m-%d')

        for category in ['Optionsscheine','Zertifikate','Faktorzertifikate']:
            resultdict = self.compare(category)
            finaldict[category] = resultdict

        FZ = finaldict['Faktorzertifikate']
        OS = finaldict['Optionsscheine']
        finaldict.pop('Faktorzertifikate')
        finaldict.pop('Optionsscheine')

        finaldict['Hebelprodukte'] = dict(chain(FZ.items(), OS.items()))
        print(finaldict)
        self.client.updateFile(finaldict, self.DDV_Mapping, eusipa)

    def readData(self, category, date):
        products = []
        with open("/Users/janickspirig/PycharmProjects/IsuanceDataService/sp-handler/data/BNP/{} {}.csv".format(
                category, date), "r",
                  encoding='ISO-8859-1') as f:
            reader = csv.reader(f, delimiter=",")

            next(reader)
            next(reader)

            for i, line in enumerate(reader):

                if "HAFTUNGSHINWEIS" in line[1]:
                    continue
                elif len(line) > 0:
                    product_id = line[1]
                    try:
                        product_type = line[2]
                    except IndexError:
                        product_type = "NotAllocated"
                    products.append([product_id, product_type])
        return products

    def convertToCSV(self, fname):
        # convert to CSV
        df = pd.read_excel("/Users/janickspirig/PycharmProjects/IsuanceDataService/sp-handler/data/BNP/{}.xlsx".format(fname))
        df.to_csv("/Users/janickspirig/PycharmProjects/IsuanceDataService/sp-handler/data/BNP/{}.csv".format(fname), sep=",")

    def compare(self, category):
        yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        today = date.today().strftime('%Y-%m-%d')

        #self.convertToCSV("{} {}".format(category, today))

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