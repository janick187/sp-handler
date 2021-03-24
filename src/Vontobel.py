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
            "1200 Discount Certificates": ["VONCORES", 'Discount-Zertifikate'],
            "1220 Reverse Convertibles": ["Express VONCERTS", "Multi VONTIS", "Multi VONTIS with low exercise price", "VONTIS", 'Aktienanleihen','Multi Aktienanleihen (Worst-Of)'],
            "1230 Barrier Reverse Convertibles": ["Defender VONCORES","Callable Multi Defender VONTIS", "Defender VONTIS", "Double Coupon Multi Defender VONTIS", "Lock-in Multi Defender VONTIS", "Multi Defender VONTIS", "Multi Defender VONTIS with Participation", 'Aktienanleihen mit Barriere','Aktienanleihen Pro mit Barriere', 'Multi Aktienanleihen mit Barriere (Worst-Of)', 'Multi Memory Express Anleihen Pro mit Barriere (Worst-Of)'],
            "1240 Capped Outperformance Certificates": ['Sprint-Zertifikate'],
            "1260 Express Certificates": ['Fixkupon Express Airbag Anleihen','Fixkupon Express Airbag Zertifikate','Fixkupon Express Anleihen mit Barriere','Fixkupon Express Anleihen Pro mit Barriere','Fixkupon Express Zertifikate mit Barriere','Fixkupon Express Zertifikate Pro mit Barriere', 'Memory Express Airbag Zertifikate','Memory Express Airbag Anleihen','Fixkupon Multi Express Anleihen mit Barriere (Worst-Of)', 'Memory Express Anleihen Pro mit Barriere', 'Memory Express Zertifikate mit Barriere', 'Memory Express Zertifikate Pro mit Barriere'],
            "1299 Miscellaneous Yield Enhancement": [],
            "1300 Tracker Certificates": ["Dynamic VONCERTS", "Strategic Certificates", "VONCERTS","VONCERTS Open End", 'Indexanleihen', 'Indexanleihen mit Barriere'],
            "1310 Outperformance Certificates": ["Capped VONCERTs Plus", "VONCERTS Plus"],
            "1320 Bonus Certificates": ["Defender VONCERTS", "Multi Defender VONCERTS", "Bonus-Zertifikate",'Bonus Cap-Zertifikate' ],
            "1399 Miscellaneous Participation": [],
            "2100 Warrants": ["Vontobel Warrants", "Open-End X-Turbo-Optionsscheine","Optionsscheine","Turbo-Optionsscheine","Turbo-Optionsscheine Open-End"],
            "2199 Miscellaneous Leverage without Knock-Out": [],
            "2200 Knock-Out Warrants": ["Sprinter-Warrants"],
            "2210 Mini-Futures": ["Vontobel Mini Futures", "Mini Futures"],
            "2299 Miscellaneous Leverage with Knock-Out": [],
            "2300 Constant Leverage Certificate": ["Factor Certificates", 'Faktor-Zertifikate'],
            "2399 Miscellaneous Leverage with Knock-Out": [],
            "1340 Twin-Win Certificates": []
        }

        self.categories = {
            'CH': {
                'Zertifikate': [
                    'Callable Multi Defender VONTIS',
                    #'Capped VONCERTs Plus',
                    'Defender VONCORES',
                    'Defender VONTIS',
                    # 'Double Coupon Multi Defender VONTIS',
                    'Dual Currency Notes',
                    'Express VONCERTS',
                    'Multi Defender VONCERTS',
                    'Multi Defender VONTIS',
                    'Multi VONTIS',
                    'Multi VONTIS with low exercise price',
                    'Strategic Certificate',
                    'Structured Product',
                    'VONCERTS',
                    'VONCERTS Open End',
                    'VONCORES',
                    'VONTIS'
                ],
                'Hebelprodukte': [
                    'Factor Certificates',
                    'Sprinters Open End',
                    #'Sprinter-Warrants',
                    'Vontobel Mini Futures',
                    'Vontobel Warrants'],
            },
            'DE': {
                'Zertifikate': [
                    'Aktienanleihen',
                    'Aktienanleihen mit Barriere',
                    #'Aktienanleihen Pro mit Barriere',
                    #'Bonus Cap-Zertifikate',
                    # 'Bonus-Zertifikate',
                    'Discount-Zertifikate',
                    #'Fixkupon Express Airbag Anleihen',
                    #'Fixkupon Express Airbag Zertifikate',
                    'Fixkupon Express Anleihen mit Barriere',
                    'Fixkupon Express Anleihen Pro mit Barriere',
                    'Fixkupon Express Zertifikate mit Barriere',
                    'Fixkupon Express Zertifikate Pro mit Barriere',
                    'Fixkupon Multi Express Airbag Anleihen (Worst-Of)',
                    #'Fixkupon Multi Express Airbag Anleihen mit Barriere (Worst-Of)',
                    'Fixkupon Multi Express Anleihen mit Barriere (Worst-Of)',
                    'Fixkupon Multi Express Zertifikate mit Barriere (Worst-Of)',
                    #'Indexanleihen',
                    #'Indexanleihen mit Barriere',
                    'Memory Express Airbag Anleihen',
                    'Memory Express Airbag Zertifikate',
                    'Memory Express Anleihen Pro mit Barriere',
                    'Memory Express Zertifikate mit Barriere',
                    'Memory Express Zertifikate Pro mit Barriere',
                    'Memory Multi Express Zertifikate mit Barriere (Worst-Of)',
                    #'Multi Aktienanleihen (Worst-Of)',
                    'Multi Aktienanleihen mit Barriere (Worst-Of)',
                    'Multi Memory Express Anleihen Pro mit Barriere (Worst-Of)',
                    'Partizipationszertifikate'
                    #'Reverse Bonus Cap-Zertifikate',
                    #'Sprint-Zertifikate'
                    ],
                'Hebelprodukte': [
                    'Faktor-Zertifikate',
                    'Mini Futures',
                    'Open-End X-Turbo-Optionsscheine',
                    'Optionsscheine',
                    'Turbo-Optionsscheine',
                    'Turbo-Optionsscheine Open-End'
                    ]
            }
        }

        for country in ['DE', 'CH']:
            self.client = ApiSheetClient("Issuance Data Collection", f"Vontobel_{country}")
            finaldict = {}
            finaldict["date"] = date.today().strftime('%Y-%m-%d')
            for category in ['Zertifikate', 'Hebelprodukte']:
                resultdict = self.compare(category, country)
                finaldict[category] = resultdict

            self.client.updateFile(finaldict, DDV_Mapping, self.EUSIPA_Mapping)

        # first create seperate CSV files or read them into different lists, depending on when next line follows...
        # I think we can do this as we have the category already saved in the list above and it follows the same order in the file

    def readData(self, date, category, country):
        products = []
        path = "/Users/janickspirig/PycharmProjects/IsuanceDataService/sp-handler/data/Vontobel_{}/{}_{}*.csv".format(country, category, date)
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
                            product_type = self.categories[country][category][product_counter]
                        except IndexError:
                            product_type = "NotAllocated"
                        products.append([product_id, product_type])
                    else:
                        # row is empty and begin with next product category
                        product_counter += 1
                        skipLine = True

        return products

    def compare(self, category, country):
        yesterday = (date.today() - timedelta(days=1)).strftime('%Y%m%d')
        today = date.today().strftime('%Y%m%d')
        oldProducts = self.readData(yesterday, category, country)
        newProducts = self.readData(today, category, country)
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