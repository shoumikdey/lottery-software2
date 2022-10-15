from venv import create
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
from random import sample

UPLOAD_FOLDER = ''

def create_separate_arrays(df):
    hindi_arr = list()
    bengali_arr = list()
    admn_no = df['admn_no'].to_list()
    sec_lang = df['sec_lang'].to_list()
    for i in range(len(sec_lang)):
        if sec_lang[i] == 'bengali':
            bengali_arr.append(admn_no[i])
        else:
            hindi_arr.append(admn_no[i])

    return hindi_arr, bengali_arr

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def lottery_maker(bengali_arr, hindi_arr, hindi_num, bengali_num):
    hindi_lottery = sample(list(hindi_arr), hindi_num)
    bengali_lottery = sample(list(bengali_arr), bengali_num)

    if (len(hindi_lottery) == len(set(hindi_lottery))) and (len(bengali_lottery) == len(set(bengali_lottery))):
        return hindi_lottery, bengali_lottery

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods = ['GET', 'POST'])
def file_up():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        print(filename)
        df = pd.read_excel(file)
        df.to_csv('lottery.csv', encoding='utf-8', index=False)
        hindi, bengali = create_separate_arrays(df)
        hindi_lottery, bengali_lottery = lottery_maker(list(bengali), list(hindi), int(request.form['hindi']), int(request.form['bengali']))
        print(len(hindi_lottery), len(bengali_lottery))
        print(request.form['hindi'], request.form['bengali'])
        return send_file('lottery.csv',  as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)