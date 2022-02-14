import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_catagories(cat , cutoff):
    cat_map = {}
    for i in range(len(cat)):
        if cat.values[i] >= cutoff:
            cat_map[cat.index[i]] = cat.index[i]
        else:
            cat_map[cat.index[i]] = 'Other'
    return cat_map

def clean_exp(x):
    if x == 'More than 50 years':
        return 50
    if x  == 'Less than 1 year':
        return 0.5
    return float(x)

def clean_edu(x):
    if "Bachelor’s degree " in x:
        return "Bachelor's degree"
    if "Master’s degree " in x:
        return "Master's degree"
    if "Professional degree" in x or "Other doctoral" in x:
        return "Post Grad"
    return "Less than a Bachelors"

@st.cache
def load_data():
    data = pd.read_csv("survey_results_public.csv")
    data = data[['Country','EdLevel','YearsCodePro','Employment','ConvertedCompYearly']]
    data = data.rename({"ConvertedCompYearly":"Salary"},axis=1)
    data = data[data['Salary'].notnull()]
    data = data.dropna()
    data = data[data["Employment"] == 'Employed full-time']
    data = data.drop('Employment',axis =1)
    country_map = shorten_catagories(data.Country.value_counts(),400)
    data['Country'] = data['Country'].map(country_map) 
    data = data[data['Salary']<=350000]
    data = data[data['Salary']>=10000]
    data = data[data['Country'] != 'Other'] 
    data['YearsCodePro'] = data['YearsCodePro'].apply(clean_exp)
    data['EdLevel'] = data['EdLevel'].apply(clean_edu)
    return data

data = load_data()

def show_explore_page():
    st.title("Explore Software Engineers' Salaries")
    st.write(
        """
        ### Stack Overflow Developer Survey 2021
        """
    )

    data1 = data['Country'].value_counts()

    fig1 , ax1 = plt.subplots()
    ax1.pie(data1 , labels = data1.index , autopct = "%1.1f" , 
    shadow = True , startangle = 90 )
    ax1.axis("equal")

    st.write(
        """
        #### Number of Data from Different Countries
        """
    )
    st.pyplot(fig1)

    st.write(
        """
        #### Mean Salary based on Countries
        """
    )
    data2 = data.groupby(['Country'])['Salary'].mean().sort_values(ascending= True)
    st.bar_chart(data2)

    st.write(
        """
        #### Mean Salary based on Exprience
        """
    )
    data2 = data.groupby(['YearsCodePro'])['Salary'].mean().sort_values(ascending= True)
    st.line_chart(data2)
