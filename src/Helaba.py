import csv
from datetime import date, timedelta
from .ApiSheetClient import ApiSheetClient

class HelabaReader:

    def __init__(self):
        self.client = ApiSheetClient("New Issuance", "Helaba")

        finaldict = {}
        finaldict["date"] = date.today().strftime('%Y-%m-%d')

        resultdict = self.compare()
        finaldict["Zertifikate"] = resultdict

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

    def readData(self, area, date):
        products = []

        if area == "Zeichnungen":
            sub_fname = "Laufende"
        else:
            sub_fname = "Gesamtuebersicht"

        with open("/Users/janickspirig/PycharmProjects/IsuanceDataService/sp-handler/data/Helaba/{} {} {}.csv".format(sub_fname, area, date), "r",
                  encoding='ISO-8859-1') as f:

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

    def compare(self):
        yesterday = (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')
        today = date.today().strftime('%d-%m-%Y')

        oldProducts = self.readData("Neuemissionen", yesterday)
        newProducts = self.readData("Neuemissionen", today)

        count_dict = {}
        for x in newProducts:
            if not any(x[0] in sl for sl in oldProducts):
                if not x[1] in count_dict.keys():
                    count_dict[x[1]] = 1
                else:
                    count_dict[x[1]] = count_dict[x[1]] + 1
        return count_dict