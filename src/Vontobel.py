import csv
import glob
from datetime import date, timedelta
from .ApiSheetClient import ApiSheetClient

class VontobelReader:

    def __init__(self, DDV_Mapping):

        self.EUSIPA_Mapping = {
            "1100 Uncapped Capital Protection": [],
            "1120 Capped Captial Protected": ["Vontobel Capped Units"],
            "1130 Capital Protection with Knock-Out": ["Shark Units"],
            "1140 Capital protection with Coupon": ["Collared Floaters"],
            "1199 Miscellaneous Capital Protection": [],
            "1200 Discount Certificates": ["VONCORES"],
            "1220 Reverse Convertibles": ["Express VONCERTS", "Multi VONTIS", "Multi VONTIS with low exercise price", "VONTIS"],
            "1230 Barrier Reverse Convertibles": ["Defender VONCORES","Callable Multi Defender VONTIS", "Defender VONTIS", "Double Coupon Multi Defender VONTIS", "Lock-in Multi Defender VONTIS", "Multi Defender VONTIS", "Multi Defender VONTIS with Participation"],
            "1260 Express Certificates": [],
            "1299 Miscellaneous Yield Enhancement": [],
            "1300 Tracker Certificates": ["Dynamic VONCERTS", "Strategic Certificates", "VONCERTS","VONCERTS Open End", ],
            "1310 Outperformance Certificates": ["Capped VONCERTs Plus", "VONCERTS Plus"],
            "1320 Bonus Certificates": ["Defender VONCERTS", "Multi Defender VONCERTS"],
            "1399 Miscellaneous Participation": [],
            "2100 Warrants": ["Vontobel Warrants"],
            "2199 Miscellaneous Leverage without Knock-Out": [],
            "2200 Knock-Out Warrants": ["Sprinter-Warrants"],
            "2210 Mini-Futures": ["Vontobel Mini Futures"],
            "2299 Miscellaneous Leverage with Knock-Out": [],
            "2300 Constant Leverage Certificate": ["Factor Certificates"],
            "2399 Miscellaneous Leverage with Knock-Out": [],
            "1340 Twin-Win Certificates": []
        }

        self.client = ApiSheetClient("New Issuance", "Vontobel")

        self.categories = {
            'Zertifikate': [
                            'Callable Multi Defender VONTIS',
                            'Capped VONCERTs Plus',
                            'Defender VONTIS',
                            #'Double Coupon Multi Defender VONTIS',
                            'Dual Currency Notes',
                            'Express VONCERTS',
                            'Multi Defender VONCERTS',
                            'Multi Defender VONTIS',
                            'Multi VONTIS',
                            'Multi VONTIS with low exercise price',
                            'Strategic Certificate',
                            'Structured Product',
                            'VONCERTS Open End',
                            #'VONCORES',
                            'VONTIS'
                            ],
            'Hebelprodukte': ['Sprinters Open End',
                              'Sprinter-Warrants',
                              'Vontobel Mini Futures',
                              'Vontobel Warrants']
        }

        finaldict = {}
        finaldict["date"] = date.today().strftime('%Y-%m-%d')
        for category in ['Zertifikate', 'Hebelprodukte']:
            resultdict = self.compare(category)
            finaldict[category] = resultdict

        self.client.updateFile(finaldict, DDV_Mapping, self.EUSIPA_Mapping)

        # first create seperate CSV files or read them into different lists, depending on when next line follows...
        # I think we can do this as we have the category already saved in the list above and it follows the same order in the file

    def readData(self, date, category):
        products = []
        path = "/Users/janickspirig/PycharmProjects/IsuanceDataService/sp-handler/data/Vontobel/{}_{}*.csv".format(category, date)
        for filename in glob.glob(path):
            with open(filename,
                      "r", encoding='ISO-8859-1') as f:
                reader = csv.reader(f, delimiter=";")
                next(reader)
                product_counter = 0
                skipLine = False
                for i, line in enumerate(reader):
                    if skipLine:
                        skipLine = False
                        continue

                    if len(line) > 0:
                        product_id = line[1].replace('\t', "")
                        try:
                            product_type = self.categories[category][product_counter]
                        except IndexError:
                            print(category)
                            print(product_counter)
                            print(line)
                            product_type = "NotAllocated"
                        products.append([product_id, product_type])
                    else:
                        # row is empty and begin with next product category
                        product_counter += 1
                        skipLine = True


        return products

    def compare(self, category):
        yesterday = (date.today() - timedelta(days=3)).strftime('%Y%m%d')
        today = date.today().strftime('%Y%m%d')
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