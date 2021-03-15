from src import *

if __name__ == '__main__':

    DDV_Mapping = {
        "1100 Kapitalschutz Zeritifikate": ["1100 Uncapped Capital Protection", "1110 Exchangeable Certificates", "1120 Capped Capital Protection", "1130 Capital Protection with Knock-Out"],
        "1140 Strukturierte Anleihen": ["1140 Capital Protection with Coupon"],
        "1199 Weitere Anlageprodukte mit Kapitalschutz": ["1199 Miscellaneous Capital Protection"],
        "1220 Aktienanleihen": ["1220 Reverse Convertibles", "1230 Barrier Reverse Convertibles"],
        "1200 Discount-Zertifikate": ["1200 Discount Certificates", "1210 Barrier Discount Certificates"],
        "1240 Sprint Zertifikate": ["1240 Capped Outperformance Certificates", "1250 Capped Bonus Certificates"],
        "1260 Express-Zertifikate": ["1260 Express Certificates", "1299 Miscellaneous Yield Enhancement"],
        "1320 Bonus Zertifikate": ["1320 Bonus Certificates", "1330 Outperformance Bonus Certificates", "1340 Twin-Win Certificates"],
        "1300 Index/-Partizipations-Zertifikate": ["1300 Tracker Certificates"],
        "1310 Outperformance-/Sprint-Zertifikate": ["1310 Outperformance Certificates"],
        "1399 Weitere Anlgeprodukte ohne Kapitalschutz": ["1399 Miscellaneous Participation"],
        "2100 Optionsscheine": ["2100 Warrants", "2110 Spread Warrants"],
        "2300 Faktor-Zertifikate": ["2300 Constant Leverage Certificate"],
        "2199 Weitere Hebelprodukte ohne Knock-Out": ["2199 Miscellaneous Leverage without Knock-Out"],
        "2200 Knock-Out Produkte": ["2200 Knock-Out Warrants", "2205 Open-end Knock-Out Warrants", "2210 Mini-Futures", "2230 Double Knock-Out Warrants"],
        "2299 Weitere Hebelprodukte mit Knock-Out": ["2299 Miscellaneous Leverage with Knock-Out"],
        "2399 Weitere Prodokute mit konstantem Hebel": ["2399 Miscellaneous Constant Leverage Products"]
    }

    #DZBankReader(DDV_Mapping)
    #LBBWReader(DDV_Mapping)
    #HelabaReader()
    #UBSReader(DDV_Mapping)
    #MorganStanleyReader(DDV_Mapping)
    #BNPReader(DDV_Mapping)
    #VontobelReader(DDV_Mapping)
    #DekaBankReader(DDV_Mapping)
    #GoldmanSachsReader()
    #CitiBankReader(DDV_Mapping)
    #HypoBankReader(DDV_Mapping)
    #HSBCReader(DDV_Mapping)
    SGReader(DDV_Mapping)
