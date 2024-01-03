from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

EXCEL_FILE_PATH = r'C:\Users\khema\excel\yes.xlsx'

def update_excel(params):
    df = pd.read_excel(EXCEL_FILE_PATH)
    new_data = pd.DataFrame([params])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_excel(EXCEL_FILE_PATH, index=False)

def search_records(params):
    df = pd.read_excel(EXCEL_FILE_PATH)

    # Initialize a mask with all True values (to retain all rows)
    mask = pd.Series([True] * len(df))

    # Apply filters based on provided parameters
    for col, val in params.items():
        mask = mask & (df[col] == val)

    filtered_df = df[mask]
    return filtered_df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    params = {
        'Parameter1': request.form['param1'],
        'Parameter2': request.form['param2'],
        'Parameter3': request.form['param3'],
        'Parameter4': request.form['param4'],
        'Parameter5': request.form['param5']
    }
    update_excel(params)
    return 'Parameters updated successfully.'

@app.route('/search', methods=['POST'])
def search():
    params = {
        'Parameter1': request.form['param1'],
        'Parameter2': request.form['param2'],
        'Parameter3': request.form['param3'],
        'Parameter4': request.form['param4'],
        'Parameter5': request.form['param5']
    }

    df = search_records(params)

    if df.empty:
        return 'No records found for the provided parameters.'

    # Prepare HTML output with search parameters and search results
    html_output = '<h3>Search Parameters:</h3>'
    html_output += '<table border="1"><tr><th>Parameter</th><th>Value</th></tr>'
    for param, value in params.items():
        html_output += f'<tr><td>{param}</td><td>{value}</td></tr>'
    html_output += '</table><br>'

    html_output += '<h3>Search Results:</h3>'
    html_output += df.to_html(index=False)
    
    return html_output

if __name__ == '__main__':
    app.run(debug=True)
