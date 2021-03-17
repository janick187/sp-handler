import csv
from datetime import date, timedelta
from .ApiSheetClient import ApiSheetClient


class DZBankReader:

    def __init__(self, DDV_Mapping):

        self.EUSIPA_Mapping = {
            "1100 Uncapped Capital Protection": [],
            "1120 Capped Captial Protected": [],
            "1130 Capital Protection with Knock-Out": [],
            "1140 Capital protection with Coupon": [],
            "1199 Miscellaneous Capital Protection": [],
            "1200 Discount Certificates": ["Discount Classic", "Discount Optionsschein Short", "Discount Optionsschein Long"],
            "1220 Reverse Convertibles": ['Aktienanleihe Classic','Aktienanleihe Protect'],
            "1230 Barrier Reverse Convertibles": [],
            "1260 Express Certificates": ['Express Classic','Express Relax', 'Index Plus','Memory Relax Express'],
            "1299 Miscellaneous Yield Enhancement": [],
            "1300 Tracker Certificates": ['Basketzertifikat','ZinsFix'],
            "1310 Outperformance Certificates": [],
            "1320 Bonus Certificates": ['Bonus Classic','Bonus Cap', 'Bonus Reverse Cap'],
            "1399 Miscellaneous Participation": [],
            "2100 Warrants": ['Optionsschein Classic Long','Optionsschein Classic Short'],
            "2199 Miscellaneous Leverage without Knock-Out": [],
            "2200 Knock-Out Warrants": ['X-Turbo Long','X-Turbo Short','Turbo Short','Mini-Future Long','Mini-Future Short','Endlos Turbo Long','Endlos Turbo Short','Turbo Long','X-Turbo Endlos Long','X-Turbo Endlos Short',],
            "2210 Mini-Futures": [],
            "2299 Miscellaneous Leverage with Knock-Out": [],
            "2300 Constant Leverage Certificate": [],
            "2399 Miscellaneous Leverage with Knock-Out": [],
            "1340 Twin-Win Certificates": []
        }


        self.client = ApiSheetClient("New Issuance", "DZBank")

        finaldict = {}
        finaldict["date"] = date.today().strftime('%Y-%m-%d')
        for category in ['Zertifikate', 'Hebelprodukte']:
            resultdict = self.compare(category)
            finaldict[category] = resultdict

        print(finaldict)
        self.client.updateFile(finaldict, DDV_Mapping, self.EUSIPA_Mapping)

    '''
    def updateFile(entry):
    
        fname = "/Users/janickspirig/Desktop/Stats/DZBankStat/results.txt"
    
        with open(fname, 'a+') as outfile:
            outfile.seek(0, 2)  # end of file
            size = outfile.tell()  # the size...
            outfile.truncate(size - 1)
            outfile.write(',')
            json.dump(entry, outfile)
            outfile.write(']')
            outfile.close()
    '''

    def readData(self, date, category):
        products = []
        with open("/Users/janickspirig/PycharmProjects/IsuanceDataService/sp-handler/data/DZBank/DZ-Bank-Produkte_{}_{}.csv".format(date, category),
                  "r", encoding='ISO-8859-1') as f:
            reader = csv.reader(f, delimiter=";")
            next(reader)
            for i, line in enumerate(reader):
                if len(line) > 0:

                    product_id = line[0].split(";")[0]
                    try:
                        product_type = line[0].split(";")[2].replace("\"", "")
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
