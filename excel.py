import xlsxwriter

workbook = xlsxwriter.Workbook('shuttleServices.xlsx')
worksheet = workbook.add_worksheet('Invoices')

# Create format objects
title_format = workbook.add_format({
    'align': 'center',
    'valign': 'vcenter',
    'bold': True,
    'border': 1
})

cell_format = workbook.add_format({
    'align': 'center',
    'valign': 'vcenter',
    'border': 1,
    'text_wrap': True
})
firstLine_format = workbook.add_format({'bg_color': 'yellow'})
orange_format = workbook.add_format({'bg_color': 'orange'})
red_format = workbook.add_format({'bg_color': 'red', 'bold': True})

worksheet.conditional_format(
    'A2:J2', {'type': 'unique', 'format': firstLine_format})
# Set up conditional formatting rules
rules = [
    {'type': 'cell', 'criteria': 'equal to',
        'value': '"Pending Add"', 'format': orange_format},
    {'type': 'cell', 'criteria': 'equal to',
        'value': '"Pending Add\nPending Add"', 'format': orange_format},
    {'type': 'cell', 'criteria': 'equal to',
        'value': '"Pending Add\nPending Add\nPending Add"', 'format': orange_format},
    {'type': 'cell', 'criteria': 'equal to', 'value': '"0"', 'format': red_format},
    {'type': 'cell', 'criteria': 'equal to',
        'value': '"Passenger Cancelled"', 'format': red_format},
    {'type': 'cell', 'criteria': 'equal to',
     'value': '"Cancelled"', 'format': red_format},
    {'type': 'cell', 'criteria': 'equal to',
        'value': '"999"', 'format': red_format},
    {'type': 'cell', 'criteria': 'equal to',
     'value': '"-999"', 'format': red_format},
    {'type': 'cell', 'criteria': 'equal to',
        'value': '"0\n0\n0\n0"', 'format': red_format},
    {'type': 'cell', 'criteria': 'equal to',
     'value': '"BLOCK"', 'format': red_format},
]

# Apply conditional formatting to the worksheet
for rule in rules:
    worksheet.conditional_format('A2:L100', rule)

# Set column widths
column_widths = {'A': 12, 'B': 12, 'C': 8, 'D': 46, 'E': 46,
                 'F': 20, 'G': 8, 'H': 8, 'I': 4, 'J': 16, 'K': 18, 'L': 18}

for column, width in column_widths.items():
    worksheet.set_column(f'{column}:{column}', width)

# Write column headers
column_headers = ['DATE', 'PICK UP TIME', 'FLIGHT', 'PICK UP', 'D|O Location',
                  'NAME', 'CREW ID', 'TRIP ID', 'PAX', 'STATUS']

worksheet.write_row(0, 0, column_headers, title_format)


# Set cells
headers = {
    "date": (1, 0),
    "time": (1, 1),
    "flight": (1, 2),
    "pick": (1, 3),
    "drop": (1, 4),
    "name": (1, 5),
    "crew": (1, 6),
    "trip": (1, 7),
    "pax": (1, 8),
    "status": (1, 9),
}


class ExcelWriter:
    def __init__(self, worksheet, headers, cell_format):
        self.worksheet = worksheet
        self.headers = headers
        self.cell_format = cell_format

        self.date_row, self.date_col = headers["date"]
        self.time_row, self.time_col = headers["time"]
        self.flight_row, self.flight_col = headers["flight"]
        self.pick_row, self.pick_col = headers["pick"]
        self.drop_row, self.drop_col = headers["drop"]
        self.name_row, self.name_col = headers["name"]
        self.crew_row, self.crew_col = headers["crew"]
        self.trip_row, self.trip_col = headers["trip"]
        self.pax_row, self.pax_col = headers["pax"]
        self.status_row, self.status_col = headers["status"]

    def write_data_to_worksheet(self, trip, pax, pdf_date, time, pick_up, flight, drop_off, crew_ids, names, statuses):
        self.worksheet.write(self.trip_row, self.trip_col,
                             trip, self.cell_format)
        self.trip_row += 1

        self.worksheet.write(self.pax_row, self.pax_col, pax, self.cell_format)
        self.pax_row += 1

        self.worksheet.write(self.date_row, self.date_col,
                             pdf_date, self.cell_format)
        self.date_row += 1

        self.worksheet.write(self.time_row, self.time_col,
                             time, self.cell_format)
        self.time_row += 1

        self.worksheet.write(self.pick_row, self.pick_col,
                             pick_up, self.cell_format)
        self.pick_row += 1

        self.worksheet.write(
            self.flight_row, self.flight_col, flight, self.cell_format)
        self.flight_row += 1

        self.worksheet.write(self.drop_row, self.drop_col,
                             drop_off, self.cell_format)
        self.drop_row += 1

        self.worksheet.write(self.crew_row, self.crew_col,
                             '\n'.join(crew_ids), self.cell_format)
        self.crew_row += 1

        self.worksheet.write(self.name_row, self.name_col,
                             '\n'.join(names), self.cell_format)
        self.name_row += 1

        self.worksheet.write(self.status_row, self.status_col,
                             '\n'.join(statuses), self.cell_format)
        self.status_row += 1
