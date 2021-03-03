import gspread
import main

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
        self.worksheet.update_cells(cell_list)

    def updateFile(self, entry, DDV_Mapping=0, eusipa_mapping=0):
        data_list = self.worksheet.get_all_values()
        date = ''
        eusipa = ""
        ddv = ""
        for key, value in entry.items():
            if key == 'date':
                date = entry[key]
            else:
                for type, number in entry[key].items():
                    # EUSIPA at second position and DDV at third position
                    if not DDV_Mapping == 0:
                        for key, value in DDV_Mapping.items():
                            for x in value:
                                if x == type:
                                    ddv = key
                                    break
                        else:
                            for key, value in eusipa_mapping.items():
                                if key == ddv:
                                    eusipa = value

                    sl = [date, eusipa, ddv, key, type, number]
                    data_list.append(sl)
        self.update_sheet(data_list)