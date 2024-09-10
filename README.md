
# Credit Risk Evaluation Using Machine Learning

This project evaluates credit risk based on historical loan data. The project includes both a Jupyter notebook for detailed analysis and an application interface built using Flask for real-time credit risk assessment.

## Project Overview

- **Credit Risk Prediction**: The project leverages machine learning models to predict the likelihood of loan default.
- **App Interface**: A web-based interface is included to allow users to evaluate credit risk using a trained model.

## Features

- **Data Analysis**: The notebook includes steps for data loading, preprocessing, and feature engineering.
- **Model Training**: Machine learning models are trained to predict the likelihood of default.
- **Web App**: A simple web interface for end-users to input loan information and get a prediction.

## Installation Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/mnbl/Credit-Risk-Evaluation
   cd Credit-Risk-Evaluation
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Project

### Option 1: Running the Jupyter Notebook

1. Open the notebook:
   ```bash
   jupyter notebook
   ```

2. Run the notebook file `Credit_Risk_Evaluation.ipynb` to explore the data and train the machine learning model.

### Option 2: Running the Flask Application

1. Navigate to the `app/Credit_Risk_Evaluation_Application/` folder.
   
2. Run the application:
   ```bash
   python app.py
   ```

3. Open your browser and navigate to `http://127.0.0.1:5000/` to interact with the credit risk evaluation tool.

## Dataset

The project uses a dataset:
- `loan_data_updated.csv`: Contains historical loan information used to train and test the machine learning models.

## Contributions

Feel free to submit pull requests or suggest improvements to enhance this project!
