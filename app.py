from flask import Flask, render_template, request
import pandas as pd
from analyze import analyze_airbnb_data
from pre_processing import pre_process_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    user_zipcode = request.form['zipcode']
    airbnb_data_path = 'data/listings+reviews+crime+attractions.csv'
    processed_data = pre_process_data(airbnb_data_path)
    if processed_data is not None:
        analysis_result = analyze_airbnb_data(processed_data, int(user_zipcode))
        return render_template('result.html', analysis_result=analysis_result)
    else:
        return "Error processing data. Please check the file path."


if __name__ == '__main__':
    app.run(debug=True)
