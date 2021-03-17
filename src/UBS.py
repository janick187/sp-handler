import csv
from datetime import date, timedelta
from .ApiSheetClient import ApiSheetClient


class UBSReader:

    def __init__(self, DDV_Mapping):

        self.EUSIPA_Mapping = {
            "1100 Uncapped Capital Protection": ['Kapitalschutz-Zertifikat mit Partizipation'],
            "1120 Capped Captial Protected": [],
            "1130 Capital Protection with Knock-Out": [],
            "1140 Capital protection with Coupon": [],
            "1199 Miscellaneous Capital Protection": [],
            "1200 Discount Certificates": ['Discount-Zertifikat'],
            "1220 Reverse Convertibles": ['Reverse Convertible'],
            "1230 Barrier Reverse Convertibles": ["BRC Callable", 'BRC Coupon at Risk','BRC Early Redemption','BRC Standard','BRC Trigger','BRC Participation', 'BRC Floating Coupon'],
            "1260 Express Certificates": ['Express-Zertifikat', "Fix Kupon Express Zertifikat"],
            "1299 Miscellaneous Yield Enhancement": ['Weitere Renditeoptimierungs-Zertifikat'],
            "1300 Tracker Certificates": ['Tracker-Zertifikat'],
            "1310 Outperformance Certificates": [],
            "1320 Bonus Certificates": ['Bonus-Zertifikat'],
            "1330 Outperformance Bonus Certificates": ['Bonus-Outperformance-Zertifikat'],
            "1340 Twin-Win Certificates": ["Twin-Win-Zertifikat"],
            "1399 Miscellaneous Participation": [],
            "2100 Warrants": ["Warrant", "Open End Turbo Optionsschein", "Turbo Optionsschein", "Standard Optionsschein", "X-Open End Turbo Optionsschein", "X-Turbo Optionsschein"],
            "2110 Spread Warrants": ['Spread Warrant'],
            "2199 Miscellaneous Leverage without Knock-Out": [],
            "2200 Knock-Out Warrants": ['Warrant mit Knock-Out'],
            "2210 Mini-Futures": ["Mini-Future", "Mini Future"],
            "2299 Miscellaneous Leverage with Knock-Out": [],
            "2300 Constant Leverage Certificate": ['Constant Leverage', "Faktor Zertifikat"],
            "2399 Miscellaneous Constant Leverage Products": ["Weitere Hebelprodukte"]
        }


        for country in ["CH", "DE"]:
            self.client = ApiSheetClient("New Issuance", f"UBS_{country}")
            finaldict = {}
            finaldict["date"] = date.today().strftime('%Y-%m-%d')
            finaldict['volumen'] = {}

            for category in ['Zertifikate', 'Hebelprodukte']:
                resultdict, volumen = self.compare(category, country)
                finaldict[category] = resultdict

                if volumen != 0:
                    finaldict['volumen'][category] = volumen

            self.client.updateFile(finaldict, DDV_Mapping, self.EUSIPA_Mapping)

    def readData(self, category, date, country):
        products = []
        with open("/Users/janickspirig/PycharmProjects/IsuanceDataService/sp-handler/data/UBS_{}/UBS-Keyinvest-Produkte_{}_{}.csv".format(
                country, date, category), "r",
                  encoding='ISO-8859-1') as f:
            reader = csv.reader(f, delimiter=",")
            next(reader)
            for i, line in enumerate(reader):
                if len(line) > 0:
                    product_id = line[1]
                    try:
                        product_type = line[0]
                    except IndexError:
                        product_type = "NotAllocated"
                    products.append([product_id, product_type])
        return products

    def compare(self, category, country):
        yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        today = date.today().strftime('%Y-%m-%d')

        oldProducts = self.readData(category, yesterday, country)
        newProducts = self.readData(category, today, country)

        count_dict = {}
        volumen = len(newProducts)
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
        return count_dict, volumen