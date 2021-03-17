import csv
from datetime import date, timedelta
from .ApiSheetClient import ApiSheetClient
import pandas as pd
from itertools import chain


class BNPReader:

    def __init__(self, DDV_Mapping):

        self.EUSIPA_Mapping = {
            "1100 Uncapped Capital Protection": [],
            "1120 Capped Captial Protected": [],
            "1130 Capital Protection with Knock-Out": [],
            "1140 Capital protection with Coupon": ['Strukturierte Anleihe'],
            "1199 Miscellaneous Capital Protection": [],
            "1200 Discount Certificates": ['Discount'],
            "1220 Reverse Convertibles": ['Aktienanleihe Classic', 'Aktienanleihe Protect', 'Aktienanleihe Protect Last Minute'],
            "1230 Barrier Reverse Convertibles": [],
            "1260 Express Certificates": ['Best Express Zertifikat', 'Express Zertifikat', 'Klassik Express Zertifikat', 'Memory Express Zertifikat'],
            "1299 Miscellaneous Yield Enhancement": [],
            "1300 Tracker Certificates": ['Indexanleihe Protect', 'Partizipationszertifikat'],
            "1310 Outperformance Certificates": [],
            "1320 Bonus Certificates": ['Reverse Bonus', 'Reverse Bonus PRO','Bonus', 'Bonus PRO', 'Capped Bonus', 'Capped Bonus PRO', 'Capped Reverse Bonus', 'Capped Reverse Bonus PRO', 'Last Minute Bonus', 'Last Minute Capped Bonus'],
            "1399 Miscellaneous Participation": [],
            "2100 Warrants": ['Put', 'Call', 'Discount-Optionsschein'],
            "2199 Miscellaneous Leverage without Knock-Out": [],
            "2200 Knock-Out Warrants": [],
            "2205 Open-end Knock-Out Warrants": ['Open End Zertifikat'],
            "2210 Mini-Futures": [],
            "2299 Miscellaneous Leverage with Knock-Out": [],
            "2300 Constant Leverage Certificate": ['Faktor Long', 'Faktor Short'],
            "2399 Miscellaneous Leverage with Knock-Out": [],
            "1340 Twin-Win Certificates": []
        }

        self.client = ApiSheetClient("New Issuance", "BNP")

        finaldict = {}
        finaldict["date"] = date.today().strftime('%Y-%m-%d')

        for category in ['Optionsscheine','Zertifikate','Faktorzertifikate', 'KnockOuts']:
            resultdict = self.compare(category)
            finaldict[category] = resultdict

        FZ = finaldict['Faktorzertifikate']
        OS = finaldict['Optionsscheine']
        KO = finaldict['KnockOuts']
        finaldict.pop('Faktorzertifikate')
        finaldict.pop('Optionsscheine')
        finaldict.pop('KnockOuts')

        finaldict['Hebelprodukte'] = dict(chain(FZ.items(), OS.items(), KO.items()))

        print(finaldict)

        self.client.updateFile(finaldict, DDV_Mapping, self.EUSIPA_Mapping)

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
        #today = date.today().strftime('%Y-%m-%d')

        self.convertToCSV("{} {}".format(category, today))

        oldProducts = self.readData(category, yesterday)
        newProducts = self.readData(category, today)

        count_dict = {}
        #count_dict['Volumen'] = len(newProducts)
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