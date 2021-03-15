import gspread
import gspread_formatting


class ApiSheetClient:

    def __init__(self, sh, ws):
        self.gc = gspread.service_account()
        self.worksheet = self.gc.open(sh).worksheet(ws)

    def numberToLetters(self, q):
        """
        Helper function to convert number of column to its index, like 10 -> 'A'
        """
        q = q - 1
        result = ''
        while q >= 0:
            remain = q % 26
            result = chr(remain + 65) + result;
            q = q // 26 - 1
        return result

    def colrow_to_A1(self, col, row):
        return self.numberToLetters(col) + str(row)

    def format_number(self):

        fmt = gspread_formatting.cellFormat(
            numberFormat=gspread_formatting.NumberFormat(type="NUMBER", pattern="#,##0" )
        )

        gspread_formatting.format_cell_ranges(self.worksheet, [('F', fmt)])

    def update_sheet(self, rows, left=1, top=1):
        """
        updates the google spreadsheet with given table
        - ws is gspread.models.Worksheet object
        - rows is a table (list of lists)
        - left is the number of the first column in the target document (beginning with 1)
        - top is the number of first row in the target document (beginning with 1)
        """

        # number of rows and columns
        num_lines, num_columns = len(rows), len(rows[0])

        # selection of the range that will be updated
        cell_list = self.worksheet.range(
            self.colrow_to_A1(left, top) + ':' + self.colrow_to_A1(left + num_columns - 1, top + num_lines - 1)
        )

        # modifying the values in the range

        for cell in cell_list:
            val = rows[cell.row - top][cell.col - left]
            cell.value = val

        # update in batch
        self.worksheet.update_cells(cell_list, 'USER_ENTERED')

    def updateFile(self, entry, DDV_Mapping=0, eusipa_mapping=0, Volumen=False, ExchangeData=False):
        data_list = self.worksheet.get_all_values()
        date = ''
        for key1, value in entry.items():
            if key1 == 'date':
                date = entry[key1]
            elif key1 == 'volumen':
                continue
            else:
                # check if key has entries otherwise it is 0!
                if len(entry[key1].items()) > 0:
                    #for type, number in entry[key1].items():
                    for type in entry[key1].keys():
                        # skip Volumen entry


                        # EUSIPA at second position and DDV at third position
                        eusipa = ""
                        ddv = ""
                        if not eusipa_mapping == 0:
                            for key2, value in eusipa_mapping.items():
                                for x in value:
                                    if x == type:
                                        eusipa = key2

                        if not eusipa == "":
                            for key3, value in DDV_Mapping.items():
                                for x in value:
                                    if x == eusipa:
                                        ddv = key3

                        ISINs = ""
                        for isin in entry[key1][type]['ISINs'][:5]:
                            ISINs += "{}, ".format(isin)
                        ISINs = ISINs[:-2]
                        if ExchangeData:
                            sl = [date, eusipa, ddv, key1, type, entry[key1][type]['amount'], ISINs, entry[key1][type]['exchange'], entry[key1][type]['not exchange'], ""]
                        else:
                            sl = [date, eusipa, ddv, key1, type, entry[key1][type]['amount'], ISINs, ""]
                        data_list.append(sl)
                else:
                    sl = [date, "", "", key1, "", "0", "", ""]
                    data_list.append(sl)

        if Volumen:
            for key, value in entry['volumen'].items():
                sl = [entry['date'], "","", key, "", "", "",value]
                data_list.append(sl)

        self.update_sheet(data_list)
        #self.format_number()