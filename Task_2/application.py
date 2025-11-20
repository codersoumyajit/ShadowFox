from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)


model = pickle.load(open("LinearRegressionModel.pkl", "rb"))
car = pd.read_csv("Cleaned Car.csv")


@app.route('/')
def index():
    companies = sorted(car['Car_Name'].unique())
    years = sorted(car['Year'].unique(), reverse=True)
    fuel_types = car['Fuel_Type'].unique()
    return render_template('index.html', companies=companies, year=years, fuel_type=fuel_types)

@app.route('/predict', methods=['POST'])
def predict():

    CarName = request.form.get('CarName')
    Year = int(request.form.get('year'))
    FuelType = request.form.get('fuel_type')
    kilometers_driven = int(request.form.get('kilo_driven'))

    input_data = pd.DataFrame({
        'Car_Name': [CarName],
        'Year': [Year],
        'Present_Price': [5.0],       
        'Kms_Driven': [kilometers_driven],
        'Fuel_Type': [FuelType],
        'Seller_Type': ['Dealer'],     
        'Transmission': ['Manual'],     
        'Owner': [0]                   
    })
    expected_columns = ['Year', 'Present_Price', 'Kms_Driven', 'Fuel_Type', 'Seller_Type', 'Transmission', 'Owner']

    for col in expected_columns:
        if col not in input_data.columns:
            input_data[col] = 0 

    input_data = input_data[expected_columns]
    prediction = model.predict(input_data)[0]
    print(f"Prediction: Rs. {prediction}")

    return f"{round(prediction, 2)} Lakh(s)"


if __name__ == "__main__":
    app.run(debug=True)
