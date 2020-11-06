import csv
from flask import Flask, render_template, request, send_file
import pandas
import time
import requests as r
import json
start = time.time()
app = Flask(__name__)
file_name = "app/uploads/Tracking_Result.csv"
result = []


@app.route("/")
def index():
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
            df = pandas.read_csv(file, sep=",")
            for i in df:
                str(i)
                track.append(i)

            for i in range(len(track)):

                print("\n"+"Record for  " + track[i])
                i = track[i]
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

                result.append(rdict)
            print(result)
            csv_col = ['activityType', 'dateWithNoSuffix', 'deliveryStatus', 'origin', 'time',
                       'orgCode',
                       'mode']
            try:
                with open(file_name, 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, csv_col)
                    for data in result:
                        writer.writerow(data)
            except IOError:
                print("I/O error")
            df = pandas.DataFrame(result, columns=csv_col)
            return render_template("index.html", text=df.to_html(), btn='download.html')

        except Exception as e:
            return render_template("index.html", text=str(e))


@app.route("/download-file/")
def download():
    return send_file("uploads/Tracking_Result.csv", attachment_filename='Tracking_Result.csv', as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
