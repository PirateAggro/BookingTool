# Install required libraries
# Run these commands in your terminal or command prompt
# pip install streamlit
# pip install gspread
# pip install oauth2client

import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_option_menu import option_menu
from datetime import datetime
from google.cloud import firestore
from itertools import islice

# Function to read data from Google Sheet
def read_google_sheet(sheet_url):
    # Use credentials to create a client to interact with Google Drive API
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("hola-407517-a0a85576df69.json", scope)
    gc = gspread.authorize(credentials)

    # Open the Google Sheet using its URL
    worksheet = gc.open_by_url(sheet_url).sheet1

    # Get the data as a Pandas DataFrame
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    return df

# Function to write data from Google Sheet
def write_google_sheet(sheet_url, values_to_add):
    # Use credentials to create a client to interact with Google Drive API
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("hola-407517-a0a85576df69.json", scope)
    gc = gspread.authorize(credentials)

    # Open the Google Sheet using its URL
    worksheet = gc.open_by_url(sheet_url).sheet1

    # Get the data as a Pandas DataFrame
    worksheet.append_rows(values_to_add)

    return "Update successful"

# Streamlit app
def app():
   
    st.title("Gestió Reserves Material")

    # Enter the published Google Sheet URL
    #sheet_url = st.text_input("Enter Google Sheet URL:")
    
    defaul_option  = ""

    sheet_url = "https://docs.google.com/spreadsheets/d/1uMANAvFf14030QZHner0incZyE2Tj9ex04Uiu1H-ldE/edit#gid=0"
    if sheet_url:
        # Read data from the Google Sheet
        df = read_google_sheet(sheet_url)

        # Display the data in Streamlit
        st.dataframe(df)

    sheet_url = "https://docs.google.com/spreadsheets/d/10OJjKforD1t0VSG1ynpa5QlQ2WbvmXDCGz8R4yxkoXM/edit#gid=0"
    if sheet_url:
        # Read data from the Google Sheet
        df2 = read_google_sheet(sheet_url)

        # Display the data in Streamlit
        #st.dataframe(df2)

    sheet_url = "https://docs.google.com/spreadsheets/d/16AbAcJcrp5RL-dEO5EjddgqJlwu9JUo-DjzS5tZlzUU/edit#gid=0"
    if sheet_url:
        # Read data from the Google Sheet
        df3 = read_google_sheet(sheet_url)

        # Display the data in Streamlit
        #st.dataframe(df3)

        # Create a radio button for exclusive options
        choice = st.radio('Select an option:', ['Selecció per codi', 'Selecció per nom'])

        # Display data based on the selected choice
        if choice == 'Selecció per codi':
            reservat_per_codi = df['Alumne'].unique()
            selected_codi = st.selectbox('Reservat per (codi):', reservat_per_codi)
            # Filter rows where the 'Column1' is greater than 10
            filtered_df = df[df['Alumne']==selected_codi]
            ambit = filtered_df['AP'].iloc[0]
            selected_nom = filtered_df['Nom'].iloc[0]
            #result_text.text(nom_get)
            
        elif choice == 'Selecció per nom':
            reservat_per_nom = df['Nom'].unique()
            selected_nom = st.selectbox('Reservat per (nom):', reservat_per_nom)
            # Filter rows where the 'Column1' is greater than 10
            filtered_df = df[df['Nom']==selected_nom]
            ambit = filtered_df['AP'].iloc[0]
            selected_codi = filtered_df['Codi'].iloc[0]
            
            #st.write(filtered_df['AP'])
        else:
            st.write("Please make a selection.")

        ambit = filtered_df['AP'].iloc[0]       

        # A partir selecció A o P, mostrar material disponible.
        if ambit == "A":        
            material_Disponible = df2[df2['TIPUS']==ambit]
        else:
            material_Disponible = df2
        
        selected_material = st.selectbox('Material a reservar:',material_Disponible)

        if selected_material!="":

            # Use st.date_input to get a date range input from the user
            start_date1 = st.date_input('Data Entrega', pd.to_datetime('today') - pd.DateOffset(days=7))
            end_date1 = st.date_input('Data Retorn', pd.to_datetime('today'))

            # Display the selected date range
            st.write(f'Selected Date Range: {start_date1} to {end_date1}')

            # Define selectable date range
            start_date = pd.to_datetime(start_date1, format='%d/%m/%Y')
            end_date = pd.to_datetime(end_date1, format='%d/%m/%Y')

        #validació si dates correcte
        #query a reserves per producte i status "open"
        filtered_df3 = df3[(df3['material_codi']==selected_material) & (df3['estat']=="obert")]
        st.dataframe(filtered_df3)
        flag_validesa_reserva = False
        dummy_flag = ""
        for index, row in filtered_df3.iterrows():
            Data_Inici = pd.to_datetime(row['data_inici_format'])
            Data_Final = pd.to_datetime(row['data_fi_format'])
            st.write(f'Codi: {row["reservat_codi"]}, Data_Inici: {row["data_inici_format"]}, Data_Final: {row["data_fi_format"]}')

            if Data_Inici <= start_date <= Data_Final or Data_Inici <= end_date <= Data_Final:
                #st.write("La reserva no és possible.")
                dummy_flag=""
            elif start_date <= Data_Inici and end_date >= Data_Final:
                #st.write("La reserva no és possible.")
                dummy_flag=""
            else:
                #st.write("Reserva ok")
                flag_validesa_reserva = True
        if flag_validesa_reserva == True:
            st.write("Reserva ok")