from flask import Flask, render_template, url_for, request
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from datetime import date as date_function
from contextlib import redirect_stdout
from flask import send_file
import pdfplumber
import excel
import regex
import re

app = Flask(__name__)

def round_time(time_string):
    x = time_string[-1]
    if(int(x) <= 5):
        return time_string[:-1] + '0'
    else:
        return time_string[:-1] + '5'

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return render_template('extract.html')

@app.route('/extract',methods=['POST', 'GET'])
def schedule():
    with pdfplumber.open("./FLLNKDRR.pdf") as pdf:
        with open('tmp.txt', 'w') as f:
            with redirect_stdout(f):
                for i in range(len(pdf.pages)):
                    text = pdf.pages[i].extract_text()

                    # TIME
                    time_matches = re.finditer(regex.time_re, text)
                    for matchNum, time in enumerate(time_matches, start=1):
                        if matchNum is 1:
                            time_one = round_time(time.group())
                        elif matchNum is 2:
                            time_two = round_time(time.group())
                        try:
                            if matchNum is 3:
                                time_three = round_time(time.group())
                        except StopIteration:
                            pass

                    # PICK UP
                    pick_matches = re.finditer(regex.pick_re, text)
                    for matchNum, pick_up in enumerate(pick_matches, start=1):
                        for groupNum in range(0, len(pick_up.groups())):
                            groupNum = groupNum + 1
                            if matchNum is 1:
                                pick_one = pick_up.group(1)[19:]
                            elif matchNum is 2:
                                pick_two = pick_up.group(1)[19:]
                            try:
                                if matchNum is 3:
                                    pick_three = pick_up.group(1)[19:]
                            except StopIteration:
                                pass

                    # DROP OFF
                    drop_matches = re.finditer(regex.drop_re, text)
                    for matchNum, drop_off in enumerate(drop_matches, start=1):
                        for groupNum in range(0, len(drop_off.groups())):
                            groupNum = groupNum + 1
                            if matchNum is 1:
                                drop_one = drop_off.group(groupNum)
                            elif matchNum is 2:
                                drop_two = drop_off.group(groupNum)
                            try:
                                if matchNum is 3:
                                    drop_three = drop_off.group(groupNum)
                            except StopIteration:
                                pass

                    # FLIGHT
                    flight_matches = re.finditer(regex.flight_re, text)
                    for matchNum, flight in enumerate(flight_matches, start=1):
                        for groupNum in range(0, len(flight.groups())):
                            groupNum = groupNum + 1
                            if matchNum is 1:
                                flight_one = flight.group(groupNum)
                            elif matchNum is 2:
                                flight_two = flight.group(groupNum)
                            try:
                                if matchNum is 3:
                                    flight_three = flight.group(groupNum)
                            except StopIteration:
                                pass

                    # PAX
                    pax_matches = re.finditer(regex.pax_re, text)
                    for matchNum, pax in enumerate(pax_matches, start=1):
                        for groupNum in range(0, len(pax.groups())):
                            groupNum = groupNum + 1
                            if matchNum is 1:
                                pax_one = pax.group(groupNum)
                            elif matchNum is 2:
                                pax_two = pax.group(groupNum)
                            try:
                                if matchNum is 3:
                                    pax_three = pax.group(groupNum)
                            except StopIteration:
                                pass

                    print(("{} {} to {} Flt {} Pax {}".format(
                            time_one, pick_one, drop_one,
                            flight_one, pax_one)))
                    print(("{} {} to {} Flt {} Pax {}".format(
                            time_two, pick_two, drop_two,
                            flight_two, pax_two)))
                    if matchNum is 3:
                        print(("{} {} to {} Flt {} Pax {}".format(
                                time_three, pick_three, drop_three,
                                flight_three, pax_three)))
                    else:
                        pass
    return render_template('organize.html')

@app.route('/organize',methods=['POST', 'GET'])
def organize():
    with open('messages.txt', 'w') as f:
        with redirect_stdout(f):
            today = datetime.now()
            tomorrow = today + timedelta(1)
            print("DATE = ", tomorrow.strftime('%d-%m-%Y'))
            # FLL
            with open('tmp.txt', 'r') as file:
                file_data = file.read()
                file_data = file_data.replace(
                    "Hilton Fort Lauderdale Marina", "Hilton")
                file_data = file_data.replace(
                    "FLL Ft. Lauderdale/Hollywood International", "FLL")
                with open('tmp.txt', 'w') as file:
                    file.write(file_data)
                for i, line in enumerate(open('tmp.txt')):
                    if regex.hilton_fll_re in line:
                        for match in re.finditer(regex.hilton_fll_re, line):
                            print(line.strip())
                    elif regex.fll_hilton_re in line:
                        print("")
                        for match in re.finditer(regex.fll_hilton_re, line):
                            print(line.strip())
            print("-------------------------------------")

            # MCO
            with open('tmp.txt', 'r') as file:
                file_data = file.read()
                file_data = file_data.replace(
                        "Florida Hotel & Conference Center", "Hotel")
                file_data = file_data.replace(
                        "MCO Orlando International", "MCO")
                with open('tmp.txt', 'w') as file:
                    file.write(file_data)
            for i, line in enumerate(open('tmp.txt')):
                if regex.hotel_mco_re in line:
                    for match in re.finditer(regex.hotel_mco_re, line):
                        print(line.strip())
                elif regex.mco_hotel_re in line:
                    print("")
                    for match in re.finditer(regex.mco_hotel_re, line):
                        print(line.strip())
            print("-------------------------------------")

            # TPA
            with open('tmp.txt', 'r') as file:
                file_data = file.read()
                file_data = file_data.replace(
                    "Embassy Suites Tampa Downtown", "Embassy")
                file_data = file_data.replace(
                    "TPA Tampa International", "TPA")
                with open('tmp.txt', 'w') as file:
                    file.write(file_data)
            for i, line in enumerate(open('tmp.txt')):
                if regex.embassy_tpa_re in line:
                    for match in re.finditer(regex.embassy_tpa_re, line):
                        print(line.strip())
                elif regex.tpa_embassy_re in line:
                    print("")
                    for match in re.finditer(regex.tpa_embassy_re, line):
                        print(line.strip())
            print("-------------------------------------")

            # MIA
            with open('tmp.txt', 'r') as file:
                file_data = file.read()
                file_data = file_data.replace(
                    "Intercontinental  Miami", "Inter")
                file_data = file_data.replace(
                    "MIA Miami International", "MIA")
                with open('tmp.txt', 'w') as file:
                    file.write(file_data)
            for i, line in enumerate(open('tmp.txt')):
                if regex.mia_inter_re in line:
                    for match in re.finditer(regex.mia_inter_re, line):
                        print(line.strip())
                elif regex.inter_mia_re in line:
                    print("")
                    for match in re.finditer(regex.inter_mia_re, line):
                        print(line.strip())
    return render_template('download.html')

@app.route('/invoices',methods=['POST', 'GET'])
def invoices():
    
    with pdfplumber.open("./FLLNKDRR.pdf") as pdf:
            for i in range(len(pdf.pages)):
                text = pdf.pages[i].extract_text()
                text = re.sub('MIA Miami International', 'MIA', text)
                text = re.sub('FLL Ft. Lauderdale/Hollywood International', 'FLL', text)
                text = re.sub('TPA Tampa International', 'TPA', text)
                text = re.sub('MCO Orlando International', 'MCO', text)
                text = re.sub('Embassy Suites Tampa Downtown', 'Embassy Suites Tampa', text)
                text = re.sub('Hilton Fort Lauderdale Marina', 'Hilton FLL Marina', text)
                text = re.sub('NotOnFile F/O', '**CANCELLED**', text)
                text = re.sub('NotOnFile CAP', '**CANCELLED**', text)

                # DATE
                today = date_function.today()
                date_matches = re.finditer(regex.date_re, text)
                for matchNum, date in enumerate(date_matches, start=1):
                    excel.worksheet.write(excel.date_row, excel.date_col, date.group() + str(-today.year))
                    excel.date_row += 1

                # TIME
                time_matches = re.finditer(regex.time_re, text)
                for matchNum, time in enumerate(time_matches, start=1):
                    excel.worksheet.write(excel.time_row, excel.time_col, time.group())
                    excel.time_row += 1

                # FLIGHT
                flight_matches = re.finditer(regex.flight_re, text)
                for matchNum, flight in enumerate(flight_matches, start=1):
                    excel.worksheet.write(excel.flight_row, excel.flight_col, flight.group())
                    excel.flight_row  += 1

                # PICK UP
                pick_matches = re.finditer(regex.pick_re, text)
                for matchNum, pick_up in enumerate(pick_matches, start=1):
                    excel.worksheet.write(excel.pick_row, excel.pick_col, pick_up.group(1)[19:])
                    excel.pick_row  += 1

                # DROP OFF
                drop_matches = re.finditer(regex.drop_re, text)
                for matchNum, drop_off in enumerate(drop_matches, start=1):
                    for groupNum in range(0, len(drop_off.groups())):
                        groupNum = groupNum + 1
                        if matchNum is 1:
                            excel.worksheet.write(excel.drop_row, excel.drop_col, drop_off.group(groupNum))
                            excel.drop_row  += 1
                        elif matchNum is 2:
                            excel.worksheet.write(excel.drop_row, excel.drop_col, drop_off.group(groupNum))
                            excel.drop_row  += 1
                        try:
                            if matchNum is 3:
                                excel.worksheet.write(excel.drop_row, excel.drop_col, drop_off.group(groupNum))
                                excel.drop_row  += 1
                        except StopIteration:
                            pass

                # NAME
                #breakpoint()
                name_matches = re.finditer(regex.name_re, text)
                lines = text.splitlines()
                for matchNum, name in enumerate(name_matches, start=1):
                    for i in range(len(lines)):
                        if name.group() in lines[i]:
                            excel.worksheet.write(excel.name_row, excel.name_col, name.group(2))
                            excel.name_row  += 1
                
                crew_matches = re.finditer(regex.crewID_re, text)
                lines = text.splitlines()
                for matchNum, crew in enumerate(crew_matches, start=1):
                    for i in range(len(lines)):
                        if crew.group() in lines[i]:
                            excel.worksheet.write(excel.crew_row, excel.crew_col, crew.group(1))
                            excel.crew_row  += 1

                # TRIP ID
                trip_matches = re.finditer(regex.trip_re, text)
                for matchNum, trip in enumerate(trip_matches, start=1):
                    excel.worksheet.write(excel.trip_row, excel.trip_col, trip.group())
                    excel.trip_row  += 1

                # PAX
                pax_matches = re.finditer(regex.pax_re, text)
                for matchNum, pax in enumerate(pax_matches, start=1):
                    excel.worksheet.write(excel.pax_row, excel.pax_col, pax.group())
                    excel.pax_row  += 1

            excel.workbook.close()
    return render_template('download.html')

@app.route('/download-messages')
def downloadMessages ():
    path = "messages.txt"
    return send_file(path, as_attachment=True)

@app.route('/download-invoices')
def downloadInvoices ():
    path = "shuttleServices.xlsx"
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)