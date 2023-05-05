import re
import pdfplumber
from excel import ExcelWriter, workbook, worksheet, headers, cell_format
from organize import excel_hotels


class PdfProcessor:
    def __init__(self, filename):
        self.filename = filename
        self.pattern = re.compile(
            '|'.join(map(re.escape, excel_hotels.keys())))
        self.first_trip_name = re.compile(
            r'(?<=-- Total --\n)([0-9]+)\s([0-9]+)(?:.*\n){1,3}PickUp: \(\b[a-zA-Z]{3}\b\) ([0-9]{2}-\b[a-zA-Z]{3}\b) (\d{1,2}:\d{2}) ([^\n\r]*) (?:Depart|Arrive): (?:Flt#:)([A-Za-z0-9_-]+|).*\nDrop Off: ([^\n\r]*)(?= @)(?:.*\n){3,5}(-?\d+)\s([a-zA-Z]+\s+[a-zA-Z]+).*(Updated|Previously CF\'ed|Pending Add|Revised|Cancelled)')
        self.remaining_names = re.compile(
            r'(-?\d+)\s([a-zA-Z]+\s+[a-zA-Z]+).*(Updated|Previously CF\'ed|Pending Add|Revised|Cancelled)')

    def process(self):
        with pdfplumber.open(self.filename) as pdf:
            num_pages = len(pdf.pages)
            # create the ExcelWriter object before the loop
            excel_writer = ExcelWriter(worksheet, headers, cell_format)
            for i in range(num_pages):
                text = pdf.pages[i].extract_text()
                text = self.pattern.sub(
                    lambda match: excel_hotels[match.group(0)], text)
                extras = re.findall(
                    r'\d{4}\n(\d*)\s*([a-zA-Z]+\s+[a-zA-Z]+).*(Updated|Previously CF\'ed|Pending Add|Revised|Cancelled)', text)
                """
                if extras:
                    print(f"Found {len(extras)} matches on page {i+1}:")
                    for extra in extras:
                        print(extra)
                """

                matches1 = self.first_trip_name.findall(text)

                # loop over the first group of matches and find the secondary matches
                for i, match1 in enumerate(matches1):
                    trip, pax, pdf_date, time, pick_up, flight, drop_off, crew_id, name, status = match1

                    # look for secondary matches only in the lines immediately following the matched line
                    if i+1 < len(matches1):
                        text_after_match = text[text.index(
                            match1[0]):text.index(matches1[i+1][0])]
                    else:
                        text_after_match = text[text.index(match1[0]):]
                    matches2 = self.remaining_names.findall(text_after_match)

                    # concatenate the names, crew ID, and statuses into a single string with a delimiter
                    names = [name.lower().title()]
                    crew_ids = [crew_id]
                    statuses = []
                    for match2 in matches2:
                        _, name, status2 = match2
                        if name.lower().title() not in names:
                            names.append(name.lower().title())

                        if match2[0] not in crew_ids:
                            crew_ids.append(match2[0])

                        statuses.append(status2)

                    excel_writer.write_data_to_worksheet(
                        trip, pax, pdf_date, time, pick_up, flight, drop_off, crew_ids, names, statuses)  # write data to the worksheet on each iteration

            workbook.close()
