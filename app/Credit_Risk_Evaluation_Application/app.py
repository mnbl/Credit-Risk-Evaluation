from flask import Flask, render_template, request
import pandas as pd
import random
import joblib

app = Flask(__name__)

# Load the models
model_scenario1 = joblib.load("./models/model_scenario1.pkl")
model_scenario2 = joblib.load("./models/model_scenario2.pkl")

def get_data(input_data):

    # Load the dataset
    file_path = './data/loan_data_updated.csv'
    dataframe = pd.read_csv(file_path)

    # Apply the specified transformations
    dataframe['applicant_gender'] = dataframe['applicant_gender'].apply(lambda x: 1 if str(x).lower() == "male" else 0)
    dataframe['applicant_education'] = dataframe['applicant_education'].apply(lambda x: 1 if str(x).lower() == "graduate" else 0)
    dataframe['applicant_employment'] = dataframe['applicant_employment'].apply(lambda x: 1 if str(x).lower() == "salaried" else 0)
    dataframe['co_applicant_employment'] = dataframe['co_applicant_employment'].apply(lambda x: 1 if str(x).lower() == "salaried" else 0)
    dataframe['applicant_credit_default'] = dataframe['applicant_credit_default'].apply(lambda x: 1 if x == False else 0)

    cols_to_encode = ['applicant_dependents', "property_area"]
    dataframe = pd.get_dummies(dataframe, columns=cols_to_encode, drop_first=True)
    
    # Drop null rows
    dataframe = dataframe.dropna()

    # Drop 'loan_id' and 'loan_status' columns
    dataframe = dataframe.drop(columns=['loan_id', 'loan_status'])
    
    # Select a random row
    random_index = random.randint(0, len(dataframe) - 1)
    random_row = dataframe.iloc[random_index].copy()

    # Replace values with provided values from input_data DataFrame
    random_row['applicant_income'] = input_data['Income'].values[0]
    random_row['applicant_credit_score'] = input_data['Credit_Score'].values[0]
    random_row['applicant_credit_history'] = input_data['Credit_History'].values[0]
    random_row['applicant_employment_history'] = input_data['Employment_History'].values[0]
    random_row['applicant_credit_default'] = not input_data['Credit_Default'].values[0]
    random_row['co_applicant'] = input_data['Co_Applicant'].values[0]
    random_row['co_applicant_credit_score'] = input_data['Co_Applicant_Credit_Score'].values[0]
    random_row['co_applicant_credit_default'] = not input_data['Co_Applicant_Credit_Default'].values[0]

    return pd.DataFrame([random_row])

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def evaluate():
    # Get form data
    loan_amount = float(request.form['loan_amount'])
    income = float(request.form['income'])
    credit_score = float(request.form['credit_score'])
    credit_history = float(request.form['credit_history'])
    employment_history = float(request.form['employment_history'])
    credit_default = request.form['credit_default'] == 'False'
    co_applicant = request.form['co_applicant'] == 'Yes'
    co_applicant_credit_score = float(request.form['co_applicant_credit_score']) if co_applicant else 0
    co_applicant_credit_default = request.form['co_applicant_credit_default'] == 'False' if co_applicant else False

    # Scenario 1
    scenario1_conditions = (income >= 2000 and credit_score >= 650 and credit_history >= 30 and employment_history >= 18 and credit_default)

    # Scenario 2
    scenario2_conditions = False
    if credit_score < 650 and credit_history < 10:
        if co_applicant:
            scenario2_conditions = co_applicant_credit_score >= 650 and co_applicant_credit_default
        else:
            scenario2_conditions = True

    # Prepare input data for models
    input_data = pd.DataFrame([{
        'Income': income,
        'Credit_Score': credit_score,
        'Credit_History': credit_history,
        'Employment_History': employment_history,
        'Credit_Default': not credit_default,
        'Loan_Amount': loan_amount,
        'Co_Applicant': True if co_applicant else False,
        'Co_Applicant_Credit_Score': co_applicant_credit_score,
        'Co_Applicant_Credit_Default': not co_applicant_credit_default
    }])

    input_data = get_data(input_data)

    # Predict using the models
    result_scenario1 = None
    result_scenario2 = None

    if scenario1_conditions:
        result_scenario1 = model_scenario1.predict(input_data)[0]
    else:
        result_scenario1 = "Rejected"

    if scenario2_conditions:
        result_scenario2 = model_scenario2.predict(input_data)[0]
    else:
        result_scenario2 = "Rejected"


    return render_template('index.html', result_scenario1=result_scenario1, result_scenario2=result_scenario2)

if __name__ == '__main__':
    app.run(debug=True)
