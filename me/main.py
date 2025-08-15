import pandas as pd
#import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Quarterly Utilizaion",layout="wide")

#Merging of two excel fles

#df1 = pd.read_excel("C://Users//egyan//Desktop//me//MONTHLY UTILIZATION RATE FOR 2024.xlsx")
#df2 = pd.read_excel("C://Users//egyan//Desktop//me//MONTHLY UTILIZATION RATE FOR 2023.XLSX")
#merge_df = pd.concat([df1, df2], ignore_index=True)
#merge_df.to_excel('merge_MONTHLY UTILIZATION RATE.xlsx',index=False)
#st.dataframe(merge_df)

#changing of datetime to only date

df = pd.read_excel("merge_MONTHLY UTILIZATION RATE.xlsx")
df["StartDate"] = pd.to_datetime(df["StartDate"])
df["EndDate"] = pd.to_datetime(df["EndDate"])
df["year"] = df["EndDate"].dt.year
df = df.sort_values(by="year")


df["StartDate"] = df["StartDate"].dt.date
df["EndDate"] = df["EndDate"].dt.date

#converting the data from str to numeric and also fron decimals to %
columns_to_convert = ['Q1','Q2','Q3','Q4']
for col in columns_to_convert:
    df[col] = pd.to_numeric(df[col])
    df[col] = df[col].apply(lambda x: "{:.2%}".format(x))
st.dataframe(df)

#creating select box
selected_CompanyName = st.selectbox("Select a CompanyName:", df["CompanyName"].unique())
filtered_df = df[df["CompanyName"] == selected_CompanyName]
years_available = filtered_df["year"].unique().tolist()

#selected_year = st.selectbox("Select a year", years_available)
st.dataframe(filtered_df)
result = []
for elvis in years_available:
    data_to_use = filtered_df[filtered_df["year"] == elvis]

    data_for_chart = data_to_use.copy()

    for col in columns_to_convert:
        data_for_chart[col] = data_for_chart[col].str.replace('%', '').astype(float)
    data_melted = data_for_chart.melt(
        id_vars=["CompanyName", "year"],
        value_vars=columns_to_convert,
        var_name="Quarter",
        value_name="Value"
    )


    quarter_order = ['Q1', 'Q2', 'Q3', 'Q4']
    data_melted['Quarter'] = pd.Categorical(data_melted['Quarter'], categories=quarter_order, ordered=True)
    data_melted = data_melted.sort_values('Quarter')


    fig = px.line(
        data_melted,
        x="Quarter",
        y="Value",
        title=f"{selected_CompanyName} - {elvis} Quarterly Data",
        markers=True,
        labels={"Value": "Percentage", "Quarter": "Quarter"},
    )
    result.append(fig)

for i in range(0, len(result), 2):
    cols = st.columns(2)
    for j in range(2):
        if i + j < len(result):
            with cols[j]:
                st.plotly_chart(result[i + j], use_container_width=True)








    
