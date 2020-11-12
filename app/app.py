import csv
from os import write
from flask import Flask, render_template, request, send_file
import pandas
import time
import requests as r
import json
start = time.time()
app = Flask(__name__)
file_name = "app/uploads/Tracking_Result.csv"


@app.route("/")
def index():
    open(file_name, 'w').close()
    return render_template("index.html")


track = []
jdata = []
rdict = {'activityType': '', 'dateWithNoSuffix': '', 'deliveryStatus': '', 'origin': '', 'time': '',
         'orgCode': '',
         'mode': ''}


@app.route('/success-table', methods=['POST'])
def success_table():
    if request.method == "POST":
        file = request.files['file']

        try:
            df = pandas.read_csv(file)
            for i in df:
                str(i)
                track.append(i)

            for k in range(len(track)):
                i = track[k]
                rdict["ID"] = track[k]
                url = "http://track.dtdc.com/ctbs-tracking/customerInterface.tr?submitName=getLoadMovementDetails&cnNo=" + \
                    str(i)
                try:
                    data = r.get(url)
                finally:

                    jdata = data.json()
                    jdata.reverse()
                    for jin in jdata:
                        for i in jin:
                            if i in rdict:
                                rdict[i] = jin[i]
                try:
                    with open(file_name, 'a') as csvfile:
                        csv_col = ['ID', 'activityType', 'dateWithNoSuffix', 'deliveryStatus', 'origin', 'time',
                                   'orgCode',
                                   'mode']

                        writer = csv.DictWriter(
                            csvfile, fieldnames=csv_col, extrasaction='ignore')
                        writer.writerow(rdict)
                except IOError:
                    print("I/O error")

            return render_template("index.html", btn='download.html')

        except Exception as e:
            return render_template("index.html", text=str(e))


@app.route("/download-file/")
def download():
    return send_file("uploads/Tracking_Result.csv", attachment_filename='Tracking_Result.csv', as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
