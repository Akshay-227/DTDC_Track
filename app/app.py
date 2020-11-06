from flask import Flask, render_template, request, send_file
import pandas
import time
import requests as r
start = time.time()
app = Flask(__name__)


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
            df = pandas.read_csv(file.stream)
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
                    print(rdict['dateWithNoSuffix']+" "+rdict['time']
                          + " "+rdict['activityType']+" ("+rdict['origin']+") "+rdict['deliveryStatus'])

                print("Latest updates are "+rdict['deliveryStatus']+" at " +
                      rdict['origin']+"( "+rdict['activityType']+")")
            df = pandas.DataFrame(rdict, index=[0])
            df.to_csv("uploads/Tracking_Result.csv")
            print(df)

            return render_template("index.html", text=df.to_html(), btn='download.html')
        except Exception as e:
            return render_template("index.html", text=str(e))


@app.route("/download-file/")
def download():
    return send_file("uploads/Tracking_Result.csv", attachment_filename='Tracking_Result.csv', as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
