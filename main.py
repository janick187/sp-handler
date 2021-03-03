# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from src import *


# Press the green button in the gutter to run the script.


if __name__ == '__main__':

    EUSIPA_Mapping = {
        "Kapitalschutzzeritifikate": "1100 Uncapped Capital Protection",
        "Strukturierte Anleihen": "1140 Capital protection with Coupon",
        "Weitere Anlageprodukte mit Kapitalschutz": "1199 Miscellaneous Capital Protection",
        "Bonitätsabhnhögige Schuldverschreibungen": "unknown",
        "Aktienanleihen": "1220 Reverse Convertibles",
        "Discount-Zertifikate": "1200 Discount Certificates",
        "Express-Zertifikate": "1260 Express Certificates",
        "Bonus-Zertifikate": "1320 Bonus Certificates",
        "Index/-Partizipations-Zertifikate": "1300 Tracker Certificates",
        "Outperofrmance-/Sprint-Zertifikate": "1310 Outperformance Certificates",
        "Weitere Anlgeprodukte ohne Kapitalschutz": "1399 Miscellaneous Participation",
        "Optionsscheine": "2100 Warrants",
        "Faktor-Zertifikate": "2300 Constant Leverage Certificate",
        "Weitere hebelprodukte ohne Knock-Out": "2199 Miscellaneous Leverage without Knock-Out",
        "Knock-Out Zertifikate":"2200 Knock-Out Warrants",
        "Weitere hebelprodukte mit Knock-Out": "2299 Miscellaneous Leverage with Knock-Out",
        "Weitere Prodokute mit konstantem Hebel": "2399 Miscellaneous Leverage with Knock-Out",
        "TBC":"TBC"
    }

    #DZBankReader(EUSIPA_Mapping)
    #LBBWReader()
    #HelabaReader()
    #UBSReader()
    #MorganStanleyReader(EUSIPA_Mapping)
    BNPReader(EUSIPA_Mapping)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
