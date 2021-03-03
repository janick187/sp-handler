import csv
from datetime import date, timedelta
from .ApiSheetClient import ApiSheetClient
import main


class DZBankReader:

    def __init__(self, eusipa):

        self.DDV_Mapping = {
            "Kapitalschutzzertifikate":[],
            "Strukturierte Anleihen":[],
            "Bonitätsabhnhögige Schuldverschreibungen":[],
            "Aktienanleihen":['Aktienanleihe Classic','Aktienanleihe Protect',],
            "Discount-Zertifikate":['Discount Classic'],
            "Express-Zertifikate":['Express Classic','Express Relax', 'Index Plus','Memory Relax Express'],
            "Bonus-Zertifikate":['Bonus Classic','Bonus Cap'],
            "Index/-Partizipations-Zertifikate":['Basketzertifikat','ZinsFix'],
            "Outperofrmance-/Sprint-Zertifikate":[],
            "Optionsscheine":['Optionsschein Classic Long','Optionsschein Classic Short'],
            "Faktor-Zertifikate":[],
            "Knock-Out Zertifikate":['X-Turbo Long','X-Turbo Short','Turbo Short','Mini-Future Long','Mini-Future Short','Endlos Turbo Long','Endlos Turbo Short','Turbo Long','X-Turbo Endlos Long','X-Turbo Endlos Short',]
        }
        self.client = ApiSheetClient("New Issuance", "DZBank")

        finaldict = {}
        finaldict["date"] = date.today().strftime('%Y-%m-%d')
        for category in ['Zertifikate', 'Hebelprodukte']:
            resultdict = self.compare(category)
            finaldict[category] = resultdict

        self.client.updateFile(finaldict, self.DDV_Mapping, eusipa)

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
                    print(line)
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
                    count_dict[x[1]] = 1
                else:
                    count_dict[x[1]] = count_dict[x[1]] + 1
        return count_dict
