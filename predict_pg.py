import streamlit as stm
import pickle
import numpy as np

def load_model():
    with open('saved_steps.pkl','rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data['model']
le_country = data['le_country']
le_edu = data['le_edu']

def show_predict_pg():
    stm.title("Software Developer Salary Prediction")
    stm.write("""### We need some information to predict the salary .""")

    countries = {
        'Sweden', 
        'Spain', 
        'Germany', 
        'Turkey', 
        'Canada', 
        'France',
        'Switzerland',
        'United Kingdom of Great Britain and Northern Ireland',
        'Russian Federation', 'Israel', 'Other',
        'United States of America', 'Brazil', 'Italy', 'Netherlands',
        'Poland',
        'India', 
        'Australia', 
        'Norway'
    }
    educations = {
        "Master's degree", 
        "Bachelor's degree", 
        'Less than a Bachelors',
        'Post Grad'
    }
    country = stm.selectbox("Country" , countries)
    education = stm.selectbox("Education Level" , educations)
    experience = stm.slider("Years of Experience" , 0 , 50 , 3)
    ok = stm.button("Calculate Salary")

    if ok:
        x = np.array([[country , education,experience]])
        x[:,0] = le_country.transform(x[:,0])
        x[:,1] = le_edu.transform(x[:,1])
        x = x.astype(float)
        salary = regressor.predict(x)
        stm.subheader(f"The estimated Salary is ${salary[0]:.2f}")