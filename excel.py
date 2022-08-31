import xlsxwriter

workbook = xlsxwriter.Workbook('shuttleServices.xlsx')
worksheet = workbook.add_worksheet('Invoices')

fll_mia_format = workbook.add_format({'bg_color': 'blue'})

first_format = workbook.add_format({'bg_color': 'yellow'})
worksheet.conditional_format('A2:I2', {'type': 'unique',
                             'format': first_format})
cancelled = workbook.add_format({'bg_color': 'red'})
worksheet.conditional_format('I2:I100', {'type': 'cell',
                              'criteria': 'equal to',
                              'value': '"0"',
                              'format': cancelled})
worksheet.conditional_format('F1:F100', {'type': 'cell',
                             'criteria': 'equal to',
                             'value': '"**CANCELLED** "',
                             'format': cancelled})
worksheet.conditional_format('F1:F100', {'type': 'cell',
                             'criteria': 'equal to',
                             'value': '"**CANCELLED** \n**CANCELLED** "',
                             'format': cancelled})
worksheet.conditional_format('F1:F100', {'type': 'cell',
                             'criteria': 'equal to',
                             'value': '"**CANCELLED** \n**CANCELLED** \n**CANCELLED** "',
                             'format': cancelled})
worksheet.conditional_format('G2:G100', {'type': 'cell',
                             'criteria': 'equal to',
                             'value': '"-999"',
                             'format': cancelled})
worksheet.conditional_format('G2:G100', {'type': 'cell',
                             'criteria': 'equal to',
                             'value': '"0"',
                             'format': cancelled})
worksheet.conditional_format('J1:J100', {'type': 'cell',
                             'criteria': 'equal to',
                             'value': '"** Cancelled **"',
                             'format': cancelled})
worksheet.conditional_format('J1:J100', {'type': 'cell',
                             'criteria': 'equal to',
                             'value': '"** Cancelled **\n** Cancelled **"',
                             'format': cancelled})
worksheet.conditional_format('J1:J100', {'type': 'cell',
                             'criteria': 'equal to',
                             'value': '"** Cancelled **\n** Cancelled **\n** Cancelled **"',
                             'format': cancelled})

title_format = workbook.add_format()
title_format.set_align('center')
title_format.set_align('vcenter')
title_format.set_bold()
title_format.set_border(style=1)

cell_format = workbook.add_format()
cell_format.set_border(style=1)
cell_format.set_align('center')
cell_format.set_align('vcenter')
cell_format.set_text_wrap()

worksheet.set_column('A:A', 12)
worksheet.set_column('B:B', 12)
worksheet.set_column('C:C', 8)
worksheet.set_column('D:D', 46)
worksheet.set_column('E:E', 46)
worksheet.set_column('F:F', 20)
worksheet.set_column('G:G', 8)
worksheet.set_column('H:H', 8)
worksheet.set_column('I:I', 4)
worksheet.set_column('J:J', 16)
worksheet.set_column('K:K', 18)
worksheet.set_column('L:L', 18)

worksheet.write('A1', 'DATE', title_format)
worksheet.write('B1', 'PICK UP TIME', title_format)
worksheet.write('C1', 'FLIGHT', title_format)
worksheet.write('D1', 'PICK UP', title_format)
worksheet.write('E1', 'D|O Location', title_format)
worksheet.write('F1', 'NAME', title_format)
worksheet.write('G1', 'CREW ID', title_format)
worksheet.write('H1', 'TRIP ID', title_format)
worksheet.write('I1', 'PAX', title_format)
worksheet.write('J1', 'STATUS', title_format)

date_row = 1
date_col = 0
time_row = 1
time_col = 1
flight_row = 1
flight_col = 2
pick_row = 1
pick_col = 3
drop_row = 1
drop_col = 4
name_row = 1
name_col = 5
crew_row = 1
crew_col = 6
trip_row = 1
trip_col = 7
pax_row = 1
pax_col = 8
status_row = 1
status_col = 9