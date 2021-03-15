import csv
from datetime import date, timedelta
from .ApiSheetClient import ApiSheetClient


class HypoBankReader:

    def __init__(self, DDV_Mapping):

        self.EUSIPA_Mapping = {
            "1100 Uncapped Capital Protection": [],
            "1120 Capped Capital Protection": [],
            "1130 Capital Protection with Knock-Out": [],
            "1140 Capital protection with Coupon": [],
            "1199 Miscellaneous Capital Protection": ["Weitere Kapitalschutz-Anleihen"],
            "1200 Discount Certificates": ["Discount-Zertifikate"],
            "1220 Reverse Convertibles": ["Aktienanleihen"],
            "1230 Barrier Reverse Convertibles": [],
            "1240 Capped Outperformance Certificates": ["Sprint-Zertifikate"],
            "1260 Express Certificates": [ "Express-Zertifikate"],
            "1299 Miscellaneous Yield Enhancement": [],
            "1300 Tracker Certificates": ["Index-/Partizipations-Zertifikate", "Indexanleihen"],
            "1310 Outperformance Certificates": [],
            "1320 Bonus Certificates": ["Bonus-Zertifikate - Cap","Bonus-Zertifikate - Klassik","Bonus-Zertifikate - Pro","Bonus-Zertifikate - Reverse Cap"],
            "1399 Miscellaneous Participation": [],
            "2100 Warrants": ["Optionsscheine-Call", "Optionsscheine-Put", "Inline Optionsscheine", "Discount Optionsscheine-Call", "Discount Optionsscheine-Put", "Stay High Optionsscheine", "Stay Low Optionsscheine"],
            "2199 Miscellaneous Leverage without Knock-Out": [],
            "2200 Knock-Out Warrants": [ "Turbo - Bear", "Turbo - Bull", "Turbo Open End - Bear", "Turbo Open End - Bull", "X-Turbo Open End - Bear", "X-Turbo Open End - Bull"],
            "2210 Mini-Futures": ["Mini Future - Bear", "Mini Future - Bull"],
            "2299 Miscellaneous Leverage with Knock-Out": [],
            "2300 Constant Leverage Certificate": ["Faktor-Zertifikate"],
            "2399 Miscellaneous Leverage with Knock-Out": [],
            "1340 Twin-Win Certificates": []
        }

        # TBC: "Floater-Anleihen", "Garant-Anleihen", "Stufenzinsanleihen", "Garant-Zertifikate", "Anleihen mit Mindestrückzahlung", "Bonitätsabhängige Schuldverschreibungen", "Fondsanleihen", "Top-Zertifikate"

        self.CATEGORY_Mapping = {
            'Hebelprodukte': ["Inline Optionsscheine",
                              "Mini Future - Bear",
                              "Mini Future - Bull",
                              "Stay High Optionsscheine",
                              "Stay Low Optionsscheine",
                              "Turbo - Bear",
                              "Turbo - Bull",
                              "Turbo Open End - Bear",
                              "Turbo Open End - Bull",
                              "X-Turbo Open End - Bear",
                              "X-Turbo Open End - Bull",
                              "Discount Optionsscheine-Call",
                              "Discount Optionsscheine-Put",
                              "Faktor-Zertifikate",
                              "Optionsscheine-Call",
                              "Optionsscheine-Put"],
            'Zertifikate': ["Floater-Anleihen",
                            "Garant-Anleihen",
                            "Stufenzinsanleihen",
                            "Weitere Kapitalschutz-Anleihen",
                            "Garant-Zertifikate",
                            "Aktienanleihen",
                            "Anleihen mit Mindestrückzahlung",
                            "Bonitätsabhängige Schuldverschreibungen",
                            "Fondsanleihen",
                            "Indexanleihen",
                            "Bonus-Zertifikate - Cap",
                            "Bonus-Zertifikate - Klassik",
                            "Bonus-Zertifikate - Pro",
                            "Bonus-Zertifikate - Reverse Cap",
                            "Discount-Zertifikate",
                            "Express-Zertifikate",
                            "Index-/Partizipations-Zertifikate",
                            "Sprint-Zertifikate",
                            "Top-Zertifikate",
                            "Weitere Zertifikate"]
        }



        self.client = ApiSheetClient("New Issuance", "Hypo")

        finaldict = {}
        finaldict["date"] = date.today().strftime('%Y-%m-%d')
        for category in ['Zertifikate', 'Hebelprodukte']:
            resultdict = self.compare(category)
            finaldict[category] = resultdict


        self.client.updateFile(finaldict, DDV_Mapping, self.EUSIPA_Mapping)

    def readData(self, category, date):
        products = []
        with open(
                "/Users/janickspirig/PycharmProjects/IsuanceDataService/sp-handler/data/Hypo/Neuemissionen_{}.csv".format(
                        date),
                "r", encoding='ISO-8859-1') as f:
            reader = csv.reader(f, delimiter=";")
            next(reader)
            next(reader)
            for i, line in enumerate(reader):
                if len(line) > 0:

                    product_id = line[0]
                    try:
                        product_type = line[1]
                    except IndexError:
                        product_type = "NotAllocated"
                    # check if product type is of this specific category
                    for key, value in self.CATEGORY_Mapping.items():
                        for t in self.CATEGORY_Mapping[key]:
                            if t == product_type:
                                if key == category:
                                    products.append([product_id, product_type])
        return products


    def compare(self, category):
        today = date.today().strftime('%Y-%m-%d')
        yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
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
