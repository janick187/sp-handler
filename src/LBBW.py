import csv
from datetime import date, timedelta
from .ApiSheetClient import ApiSheetClient


class LBBWReader:

    def __init__(self):
        self.client = ApiSheetClient("New Issuance", "LBBW")

        finaldict = {}
        finaldict["date"] = date.today().strftime('%Y-%m-%d')

        for category in ['Zertifikate']:
            resultdict = self.compare(category)
            finaldict[category] = resultdict

        print(finaldict)

        self.client.updateFile(finaldict)

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

    def readData(self, area, date, category):
        products = []
        with open(
                "/Users/janickspirig/PycharmProjects/IsuanceDataService/sp-handler/data/LBBW/{}-{}-{}.csv".format(area, category, date), "r", encoding='ISO-8859-1') as f:
            reader = csv.reader(f, delimiter=";")
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

    def compare(self, category):
        yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        today = date.today().strftime('%Y-%m-%d')

        oldProducts = self.readData("Neuemissionen", yesterday, category)
        newProducts = self.readData("Neuemissionen", today, category)

        count_dict = {}
        for x in newProducts:
            if not any(x[0] in sl for sl in oldProducts):
                if not x[1] in count_dict.keys():
                    count_dict[x[1]] = 1
                else:
                    count_dict[x[1]] = count_dict[x[1]] + 1
        return count_dict
