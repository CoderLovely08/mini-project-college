from flask import Flask, render_template, redirect, url_for, request, send_file, jsonify
from werkzeug.utils import secure_filename
import os
import pandas as pd
import re
import test
from api import generate_query
# df = pd.read_excel('superstore.xlsx')

app = Flask(__name__, static_url_path='/static')
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'xlsx', 'xls', 'csv'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

dataFrame = ''


@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/upload', methods=['GET'])
def upload():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def uploadSheet():
    try:
        file = request.files['file']
        if file.filename == '':
            return render_template("index.html", error="File is required")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], "inputfile.xlsx")
            file.save(file_path)
            file = open('meta.txt', 'w')
            file.write('False')
            file.close()
            return redirect(url_for('viewData'))
        else:
            return render_template("index.html", error="Invalid file format")
    except Exception as e:
        print("Error in ", e)


@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return 'File not found.'


@app.route('/datatable', methods = ['GET'])
def viewData():
    try:
        # Check if file already exists or not
        # data = test.fetchAllData()
        # if(len(data[0]) >=1 ):
        #     print("File found in cache!")
        #     return render_template('data.html', data = data[0], columns=data[1])
        # else:
        global dataFrame
        dataFrame = test.readDataFile("inputfile")
        createTable = test.createDataTable(dataFrame)
        if(createTable == 0):
            file = open('meta.txt', 'w')
            file.write('True')
            data = test.fetchAllData()
            file.close()
            return render_template('data.html', data = data[0], columns=data[1])
        elif createTable == 1: 
            return render_template("error.html")
    except Exception as e:
        print("Error", e)
        return render_template("error.html")


@app.route('/generate_graph', methods=['POST'])
def generate_graph():
    global dataFrame
    chartId = int(request.form['chartId'])
    xLabel = request.form['xLabel']
    yLabel = request.form['yLabel']
    # filename = test.createCharts(chartId, xLabel, yLabel, dataFrame)
    # Testing new function for chart creation
    filename = test.createChart(chartId, xLabel, yLabel, dataFrame)
    return jsonify({'filename': filename})

@app.route('/get_graph', methods=['POST'])
def get_graph():
    global dataFrame
    chartId = int(request.form['chartId'])
    filename = test.getChartName(chartId)
    return jsonify({'filename': filename})


@app.route('/generateQuery', methods=['GET'])
def get_columns():
    userQuery = request.args.get('query')
    result = generate_query(userQuery)
    return jsonify({"responseQuery":result})


@app.route('/runQuery', methods=['GET'])
def run_query():

    userQuery = request.args.get('data')
    result = test.runQuery(userQuery)
    return render_template('queryTest.html', data = result[0], columns=result[1], query = result[2])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)