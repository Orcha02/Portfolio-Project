from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

from organize import hotels_location
from write_invoices import PdfProcessor
from write_messages import (
    PDFExtractor,
    FileWriter,
    replace_hotel_names,
    filter_hotels
)

app = Flask(__name__)


def round_time(time_string):
    x = time_string[-1]
    if (int(x) <= 5):
        return time_string[:-1] + '0'
    else:
        return time_string[:-1] + '5'


@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")


@app.route('/menu', methods=['POST', 'GET'])
def menu():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
    return render_template("menu.html")


@app.route('/messages', methods=['POST', 'GET'])
def messages():
    # write messages
    pdf_extractor = PDFExtractor('./FLLNKDRR.pdf')
    data = pdf_extractor.extract_data()
    file_writer = FileWriter()
    file_writer.write_data(data)
    file_data = file_writer.get_data()
    file_data = replace_hotel_names(file_data)
    filter_hotels(file_data, hotels_location)
    return render_template('messages.html')


@app.route('/invoices', methods=['POST', 'GET'])
def invoices():
    filename = './FLLNKDRR.pdf'
    processor = PdfProcessor(filename)
    processor.process()
    return render_template('download.html')


@app.route('/download-messages')
def downloadMessages():
    path = "messages.txt"
    return send_file(path, as_attachment=True)


@app.route('/download-invoices')
def downloadInvoices():
    path = "shuttleServices.xlsx"
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
