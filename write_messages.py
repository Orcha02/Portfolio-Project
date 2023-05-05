import os
import re
from datetime import datetime, timedelta
from io import StringIO

import pdfplumber
from django.conf import settings

from organize import shorter_names


class PDFExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.regex = re.compile(
            r'(?<=-- Total --\n).*\s([0-9]+)(?:.*\n){1,3}PickUp: \(\b[a-zA-Z]{3}\b\) ([0-9]{2}-\b[a-zA-Z]{3}\b) (\d{1,2}:\d{2}) ([^\n\r]*) (?:Depart|Arrive): (?:Flt#:)([A-Za-z0-9_-]+|).*\nDrop Off: ([^\n\r]*)(?= @)')

    def extract_data(self):
        with pdfplumber.open(self.pdf_path) as pdf:
            data = []
            for page in pdf.pages:
                text = page.extract_text()
                matches = self.regex.findall(text)
                for match in matches:
                    data.append({
                        'pax': match[0],
                        'date': match[1],
                        'time': match[2],
                        'pickup': match[3],
                        'flight': match[4],
                        'dropoff': match[5],
                    })
        return data


class FileWriter:
    def __init__(self):
        self.buffer = StringIO()

    def write_data(self, data):
        for matches in data:
            self.buffer.write(
                f"{matches['time']} {matches['pickup']} to {matches['dropoff']} Flt {matches['flight']} Pax {matches['pax']}\n")

    def get_data(self):
        return self.buffer.getvalue()


def replace_hotel_names(file_data):
    for old, new in shorter_names.items():
        file_data = file_data.replace(old, new)
    return file_data


def filter_hotels(file_data, hotels_data):
    tomorrow = datetime.now() + timedelta(1)
    with open("messages.txt", 'w') as f:
        for city, hotels in hotels_data.items():
            city_pattern = re.compile('|'.join(re.escape(h) for h in hotels))
            city_hotels = []
            for line in file_data.splitlines():
                if city_pattern.search(line):
                    city_hotels.append(line.strip())
            if city_hotels:
                f.write(f"{tomorrow.strftime('%B %d')} #{city}\n\n")
                f.write('\n'.join(city_hotels) + '\n')
                f.write("--------------------------------------------------------\n")
        f.write(f"{tomorrow.strftime('%B %d')} **LIMOS**\n\n")
        locals = set(h for hotels in hotels_data.values() for h in hotels)
        for line in file_data.splitlines():
            if not any(local in line for local in locals):
                f.write(line.strip() + '\n')
