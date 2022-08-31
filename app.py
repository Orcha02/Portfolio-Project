from flask import Flask, render_template, url_for, request, send_file
from datetime import date, datetime, timedelta
from werkzeug.utils import secure_filename
from contextlib import redirect_stdout
import pdfplumber
import excel
import re
import r

todays_date = date.today()
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
                    time_matches = re.finditer(r.time_re, text)
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
                    pick_matches = re.finditer(r.pick_re, text)
                    for matchNum, pick_up in enumerate(pick_matches, start=1):
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
                    drop_matches = re.finditer(r.drop_re, text)
                    for matchNum, drop_off in enumerate(drop_matches, start=1):
                        if matchNum is 1:
                            drop_one = drop_off.group(1)
                        elif matchNum is 2:
                            drop_two = drop_off.group(1)
                        try:
                            if matchNum is 3:
                                drop_three = drop_off.group(1)
                        except StopIteration:
                            pass

                    # FLIGHT
                    flight_matches = re.finditer(r.flight_re, text)
                    for matchNum, flight in enumerate(flight_matches, start=1):
                        if matchNum is 1:
                            flight_one = flight.group(1)
                        elif matchNum is 2:
                            flight_two = flight.group(1)
                        try:
                            if matchNum is 3:
                                flight_three = flight.group(1)
                        except StopIteration:
                            pass

                    # PAX
                    pax_matches = re.finditer(r.pax_re, text)
                    for matchNum, pax in enumerate(pax_matches, start=1):
                        if matchNum is 1:
                            pax_one = pax.group(1)
                        elif matchNum is 2:
                            pax_two = pax.group(1)
                        try:
                            if matchNum is 3:
                                pax_three = pax.group(1)
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
            with open('tmp.txt', 'r') as file:
                file_data = file.read()
                file_data = file_data.replace(
                    "Hilton Fort Lauderdale Marina", "Hilton")
                file_data = file_data.replace(
                    "FLL Ft. Lauderdale/Hollywood International", "FLL")
                file_data = file_data.replace(
                    "Wyndham Garden Ft Lauderdale Airport & Cruise Port",
                    "Wyndham Garden FLL")
                file_data = file_data.replace(
                    "Sheraton Suites Plantation",
                    "Sheraton FLL")
                file_data = file_data.replace(
                    "Hyatt Place Fort Lauderdale Cruise Port",
                    "Hyatt Place FLL")
                file_data = file_data.replace(
                    "Renaissance Ft. Lauderdale",
                    "Renaissance FLL")
                file_data = file_data.replace(
                    "Florida Hotel & Conference Center", "Hotel")
                file_data = file_data.replace(
                    "MCO Orlando International", "MCO")
                file_data = file_data.replace(
                    "Fairfield Inn by Marriott Orlando Airport",
                    "Fairfield Inn MCO Airport")
                file_data = file_data.replace(
                    "Element Orlando International Drive",
                    "Element Orlando")
                file_data = file_data.replace(
                    "Sheraton Suites Orlando Airport",
                    "Sheraton Orlando")
                file_data = file_data.replace(
                    "Doubletree by Hilton Orlando Airport",
                    "DoubleTree MCO Airport")
                file_data = file_data.replace(
                    "DoubleTree by Hilton Orlando at SeaWorld",
                    "DoubleTree MCO at SeaWorld")
                file_data = file_data.replace(
                    "Embassy Suites Tampa Downtown", "Embassy")
                file_data = file_data.replace(
                    "TPA Tampa International", "TPA")
                file_data = file_data.replace(
                    "Courtyard by Marriott Tampa Westshore/Airport",
                    "Courtyard by Marriott Tampa")
                file_data = file_data.replace(
                    "RENAISSANCE TAMPA PLAZA",
                    "Renaissance Tampa Plaza")
                file_data = file_data.replace(
                    "Intercontinental  Miami", "Inter")
                file_data = file_data.replace(
                    "MIA Miami International", "MIA")
                file_data = file_data.replace(
                    "Hampton Inn Miami- Airport West",
                    "Hampton Inn Miami Airport West")
                file_data = file_data.replace(
                    "EB HOTEL", "EB Hotel")

                with open('tmp.txt', 'w') as file:
                    file.write(file_data)
                print(tomorrow.strftime("%B %d"))  # FLL
                for i, line in enumerate(open('tmp.txt')):
                    if r.hilton_fll_re in line:
                        for match in re.finditer(r.hilton_fll_re, line):
                            print(line.strip())
                    elif r.fll_hilton_re in line:
                        print("")
                        for match in re.finditer(r.fll_hilton_re, line):
                            print(line.strip())
                    elif r.fll_sheratonFll_re in line:
                        for match in re.finditer(r.fll_sheratonFll_re, line):
                            print("")
                            print(line.strip())
                    elif r.sheratonFll_fll_re in line:
                        for match in re.finditer(r.sheratonFll_fll_re, line):
                            print("")
                            print(line.strip())
                    elif r.fll_hyatt_re in line:
                        for match in re.finditer(r.fll_hyatt_re, line):
                            print("")
                            print(line.strip())
                    elif r.hyatt_fll_re in line:
                        for match in re.finditer(r.hyatt_fll_re, line):
                            print("")
                            print(line.strip())
                    elif r.fll_wyndham_re in line:
                        for match in re.finditer(r.fll_wyndham_re, line):
                            print("")
                            print(line.strip())
                    elif r.wyndham_fll_re in line:
                        for match in re.finditer(r.wyndham_fll_re, line):
                            print("")
                            print(line.strip())
                print("-------------------------------------")
                print(tomorrow.strftime("%B %d"))  # MCO
                for i, line in enumerate(open('tmp.txt')):
                    if r.hotel_mco_re in line:
                        for match in re.finditer(r.hotel_mco_re, line):
                            print(line.strip())
                    elif r.mco_hotel_re in line:
                        print("")
                        for match in re.finditer(r.mco_hotel_re, line):
                            print(line.strip())
                    elif r.element_mco_re in line:
                        print("")
                        for match in re.finditer(r.element_mco_re, line):
                            print(line.strip())
                    elif r.mco_element_re in line:
                        print("")
                        for match in re.finditer(r.mco_element_re, line):
                            print(line.strip())
                    elif r.sheratonMco_mco_re in line:
                        print("")
                        for match in re.finditer(r.sheratonMco_mco_re, line):
                            print(line.strip())
                    elif r.mco_sheratonMco_re in line:
                        print("")
                        for match in re.finditer(r.mco_sheratonMco_re, line):
                            print(line.strip())
                    elif r.dtMco_mco_re in line:
                        print("")
                        for match in re.finditer(r.dtMco_mco_re, line):
                            print(line.strip())
                    elif r.mco_dtMco_re in line:
                        print("")
                        for match in re.finditer(r.mco_dtMco_re, line):
                            print(line.strip())
                    elif r.dtSeaworld_mco_re in line:
                        print("")
                        for match in re.finditer(r.dtSeaworld_mco_re, line):
                            print(line.strip())
                    elif r.mco_dtSeaworld_re in line:
                        print("")
                        for match in re.finditer(r.mco_dtSeaworld_re, line):
                            print(line.strip())
                    elif r.mco_fairfield_re in line:
                        print("")
                        for match in re.finditer(r.mco_fairfield_re, line):
                            print(line.strip())
                    elif r.fairfield_mco_re in line:
                        for match in re.finditer(r.fairfield_mco_re, line):
                            print(line.strip())
                    elif r.crowne_mco_re in line:
                        print("")
                        for match in re.finditer(r.crowne_mco_re, line):
                            print(line.strip())
                    elif r.mco_crowne_re in line:
                        for match in re.finditer(r.mco_crowne_re, line):
                            print(line.strip())
                print("-------------------------------------")
                print(tomorrow.strftime("%B %d"))  # TPA
                for i, line in enumerate(open('tmp.txt')):
                    if r.embassy_tpa_re in line:
                        for match in re.finditer(r.embassy_tpa_re, line):
                            print(line.strip())
                    elif r.tpa_embassy_re in line:
                        print("")
                        for match in re.finditer(r.tpa_embassy_re, line):
                            print(line.strip())
                    elif r.tpaPlaza_tpa_re in line:
                        print("")
                        for match in re.finditer(r.tpaPlaza_tpa_re, line):
                            print(line.strip())
                    elif r.tpa_tpaPlaza_re in line:
                        print("")
                        for match in re.finditer(r.tpa_tpaPlaza_re, line):
                            print(line.strip())
                    elif r.ac_tpa_re in line:
                        print("")
                        for match in re.finditer(r.ac_tpa_re, line):
                            print(line.strip())
                    elif r.tpa_ac_re in line:
                        print("")
                        for match in re.finditer(r.tpa_ac_re, line):
                            print(line.strip())
                    elif r.hyattTPA_tpa in line:
                        print("")
                        for match in re.finditer(r.hyattTPA_tpa, line):
                            print(line.strip())
                    elif r.tpa_hyattTPA in line:
                        print("")
                        for match in re.finditer(r.tpa_hyattTPA, line):
                            print(line.strip())
                print("-------------------------------------")
                print(tomorrow.strftime("%B %d"))  # MIA
                for i, line in enumerate(open('tmp.txt')):
                    if r.mia_inter_re in line:
                        for match in re.finditer(r.mia_inter_re, line):
                            print(line.strip())
                    elif r.inter_mia_re in line:
                        print("")
                        for match in re.finditer(r.inter_mia_re, line):
                            print(line.strip())
                    elif r.hamptonMia_mia_re in line:
                        print("")
                        for match in re.finditer(r.hamptonMia_mia_re, line):
                            print(line.strip())
                    elif r.mia_hamptonMia_re in line:
                        print("")
                        for match in re.finditer(r.mia_hamptonMia_re, line):
                            print(line.strip())
                print("-------------------------------------")  # LIMOS
                print("{} **LIMOS**".format(tomorrow.strftime("%B %d")))
                cities = [r.hilton_fll_re, r.fll_hilton_re,
                          r.fll_sheratonFll_re, r.sheratonFll_fll_re,
                          r.fll_hyatt_re, r.hyatt_fll_re, r.wyndham_fll_re,
                          r.fll_wyndham_re, r.hotel_mco_re, r.mco_hotel_re,
                          r.element_mco_re, r.mco_element_re,
                          r.sheratonMco_mco_re, r.mco_sheratonMco_re,
                          r.dtMco_mco_re, r.mco_dtMco_re, r.dtSeaworld_mco_re,
                          r.mco_dtSeaworld_re, r.mco_fairfield_re,
                          r.fairfield_mco_re, r.embassy_tpa_re,
                          r.crowne_mco_re, r.mco_crowne_re,
                          r.tpa_embassy_re, r.tpaPlaza_tpa_re,
                          r.tpa_tpaPlaza_re, r.tpa_courtyard_re,
                          r.courtyard_tpa_re, r.ac_tpa_re, r.tpa_ac_re,
                          r.hyattTPA_tpa, r.tpa_hyattTPA,
                          r.inter_mia_re, r.mia_inter_re, r.hamptonMia_mia_re,
                          r.mia_hamptonMia_re, r.eb_mia_re, r.mia_eb_re]
                for i, line in enumerate(open('tmp.txt')):
                    if any(x in line for x in cities):
                        pass
                    else:
                        print(line.strip())
    return render_template('download.html')

@app.route('/invoices',methods=['POST', 'GET'])
def invoices():
    
    with pdfplumber.open("./FLLNKDRR.pdf") as pdf:
        for i in range(len(pdf.pages)):
            text = pdf.pages[i].extract_text()
            text = re.sub('MIA Miami International', 'MIA', text)
            text = re.sub('FLL Ft. Lauderdale/Hollywood International',
                          'FLL', text)
            text = re.sub('TPA Tampa International', 'TPA', text)
            text = re.sub('MCO Orlando International', 'MCO', text)
            text = re.sub('Embassy Suites Tampa Downtown',
                          'Embassy Suites Tampa', text)
            text = re.sub('Hilton Fort Lauderdale Marina',
                          'Hilton FLL Marina', text)
            text = re.sub('NotOnFile', '**CANCELLED**', text)

            # DATE
            date_matches = re.finditer(r.date_re, text)
            for date in date_matches:
                excel.worksheet.write(excel.date_row,
                                      excel.date_col, date.group() +
                                      str(-todays_date.year),
                                      excel.cell_format)
                excel.date_row += 1

            # TIME
            time_matches = re.finditer(r.time_re, text)
            for time in time_matches:
                excel.worksheet.write(excel.time_row, excel.time_col,
                                      time.group(), excel.cell_format)
                excel.time_row += 1

            # FLIGHT
            flight_matches = re.finditer(r.flight_re, text)
            for flight in flight_matches:
                excel.worksheet.write(excel.flight_row,
                                      excel.flight_col, flight.group(),
                                      excel.cell_format)
                excel.flight_row += 1

            # PICK UP
            pick_matches = re.finditer(r.pick_re, text)
            for pick_up in pick_matches:
                excel.worksheet.write(excel.pick_row, excel.pick_col,
                                      pick_up.group(1)[19:],
                                      excel.cell_format)
                excel.pick_row += 1

            # DROP OFF
            drop_matches = re.finditer(r.drop_re, text)
            for drop_off in drop_matches:
                excel.worksheet.write(excel.drop_row,
                                      excel.drop_col,
                                      drop_off.group(1), excel.cell_format)
                excel.drop_row += 1

            # NAME
            name_matches = re.finditer(r.name_re, text)    
            matchNum = 0
            for name in name_matches:
                if name.group(2):
                    matchNum += 1
                    if matchNum is 1:
                        one = name.group(2).lower().title()
                        excel.worksheet.write(excel.name_row, excel.name_col,
                                                                        one, excel.cell_format)
                        excel.name_row += 1
                    elif matchNum is 2:
                        two = name.group(2).lower().title()
                        excel.name_row -= 1
                        excel.worksheet.write(excel.name_row, excel.name_col,
                                              "{}\n{}".format(one, two),
                                              excel.cell_format)
                        excel.name_row += 1
                    elif matchNum is 3:
                        three = name.group(2).lower().title()
                        excel.name_row -= 1
                        excel.worksheet.write(excel.name_row, excel.name_col,
                                              "{}\n{}\n{}".format
                                              (one, two, three),
                                              excel.cell_format)
                        excel.name_row += 1
                    elif matchNum is 4:
                        four = name.group(2).lower().title()
                        excel.name_row -= 1
                        excel.worksheet.write(excel.name_row, excel.name_col,
                                              "{}\n{}\n{}\n{}".format
                                              (one, two, three, four),
                                              excel.cell_format)
                        excel.name_row += 1
                elif name.group(3):
                    matchNum = 0

            # CREW ID
            crew_matches = re.finditer(r.crewID_re, text)
            matchNum = 0
            for crew in crew_matches:
                if crew.group(1):
                    matchNum += 1
                    if matchNum is 1:
                        one = crew.group(1)
                        excel.worksheet.write(excel.crew_row, excel.crew_col,
                                              one, excel.cell_format)
                        excel.crew_row += 1
                    elif matchNum is 2:
                        two = crew.group(1)
                        excel.crew_row -= 1
                        excel.worksheet.write(excel.crew_row, excel.crew_col,
                                              "{}\n{}".format(one, two),
                                              excel.cell_format)
                        excel.crew_row += 1
                    elif matchNum is 3:
                        three = crew.group(1)
                        excel.crew_row -= 1
                        excel.worksheet.write(excel.crew_row, excel.crew_col,
                                              "{}\n{}\n{}".format
                                              (one, two, three),
                                              excel.cell_format)
                        excel.crew_row += 1
                    elif matchNum is 4:
                        four = crew.group(1)
                        excel.crew_row -= 1
                        excel.worksheet.write(excel.crew_row, excel.crew_col,
                                              "{}\n{}\n{}\n{}".format
                                              (one, two, three, four),
                                              excel.cell_format)
                        excel.crew_row += 1
                elif crew.group():
                    matchNum = 0

            # TRIP ID
            trip_matches = re.finditer(r.trip_re, text)
            for trip in trip_matches:
                excel.worksheet.write(excel.trip_row, excel.trip_col,
                                      trip.group(), excel.cell_format)
                excel.trip_row += 1

            # PAX
            pax_matches = re.finditer(r.pax_re, text)
            for pax in pax_matches:
                excel.worksheet.write(excel.pax_row, excel.pax_col,
                                      pax.group(), excel.cell_format)
                excel.pax_row += 1

            # DRR TIME
            drr_matches = re.finditer(r.drr_re, text)
            for drr in drr_matches:
               drr_time = drr.group(1)

            # STATUS
            status_matches = re.finditer(r.status_re, text)
            matchNum = 0
            for status in status_matches:
                if status.group(4):
                    matchNum += 1
                    if matchNum is 1: 
                        one = status.group(4)   
                        excel.worksheet.write(excel.status_row, excel.status_col,
                                            status.group(4), excel.cell_format)
                        excel.status_row += 1
                    elif matchNum is 2:
                        two = status.group(4)
                        excel.status_row -= 1
                        excel.worksheet.write(excel.status_row, excel.status_col,
                                              "{}\n{}".format(one, two),
                                              excel.cell_format)
                        excel.status_row += 1
                    elif matchNum is 3:
                        three = status.group(4)
                        excel.status_row -= 1 
                        excel.worksheet.write(excel.status_row, excel.status_col,
                                              "{}\n{}\n{}".format
                                              (one, two, three),
                                              excel.cell_format)
                        excel.status_row += 1
                    elif matchNum is 4:
                        four = status.group(4)
                        excel.status_row -= 1
                        excel.worksheet.write(excel.status_row, excel.status_col,
                                              "{}\n{}\n{}\n{}".format
                                              (one, two, three, four),
                                              excel.cell_format)
                        excel.status_row += 1
                elif status.group():
                    matchNum = 0

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