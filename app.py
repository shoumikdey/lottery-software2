from venv import create
from flask import Flask, render_template, request, send_file, session
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
from random import sample, seed
import datetime

UPLOAD_FOLDER = ''

def create_separate_arrays(df):
    hindi_arr = list()
    bengali_arr = list()
    admn_no = df['application_number'].to_list()
    sec_lang = df['second_language'].to_list()
    for i in range(len(sec_lang)):
        if sec_lang[i].lower() == 'bengali':
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
        seed(int(datetime.date.today().year))
        filename_download = 'final_lottery_'+str(datetime.datetime.now())+'.xlsx'
        if (request.files['file'].filename == '') or (request.form['hindi'] == '') or (request.form['bengali'] ==  ''):
            return "One more field was left empty. Please refresh the site"
        file = request.files['file']
        filename = secure_filename(file.filename)
        print(filename)
        df = pd.read_excel(file)
        hindi, bengali = create_separate_arrays(df)
        if (len(hindi) < int(request.form['hindi'])) or (len(bengali) < int(request.form['bengali'])):
            return "Sample size requested is larger than population database. Please refresh the site"

        if not ((len(hindi) == len(set(hindi))) and (len(bengali) == len(set(bengali)))):
            return "Duplicates Found, Please refresh the page and try again"

        hindi_lottery, bengali_lottery = lottery_maker(list(bengali), list(hindi), int(request.form['hindi']), int(request.form['bengali']))
        final_list = bengali_lottery + hindi_lottery
        languages = (['bengali'] * len(bengali_lottery)) + (['hindi'] * len(hindi_lottery))
        df_final = pd.DataFrame(list(zip(final_list, languages)), columns=['admn_no', 'sec_lang'])
        df_final.to_excel('final_lottery.xlsx')
        return send_file('final_lottery.xlsx',  as_attachment=True, download_name=filename_download)


if __name__ == '__main__':
    app.run(debug=True)