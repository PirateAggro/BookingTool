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

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("firestore-key.json")


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
   
    st.title("Actualització Dades Mestres")

    # Enter the published Google Sheet URL
    #sheet_url = st.text_input("Enter Google Sheet URL:")
    
    defaul_option  = ""

    sheet_url = "https://docs.google.com/spreadsheets/d/10OJjKforD1t0VSG1ynpa5QlQ2WbvmXDCGz8R4yxkoXM/edit#gid=0"
    if sheet_url:
        # Read data from the Google Sheet
        df = read_google_sheet(sheet_url)
        #clau = '99998'
        #doc_ref = db.collection("clients").document(clau)
        for index, row in df.iterrows():
        ##    st.write(row['Alumne'])
        ##    st.write(row['Nom'])
            document_id = str(row['Codi'])  # Replace 'YourIDColumn' with the actual column name
            cd = row["Codi"]
            prd = row["Producte"]
            dsc = row["Descripció"]
            stk = row["Stock"]
            amb = row["TIPUS"]
            ##tps = row["Tipus"]
            ##doc_ref = db.collection("Clients").document(str(row["Alumne"]))
            # Adding a document to the "Clients" collection with an auto-generated document ID
            if cd != "":
                ##doc_ref = db.collection('Productes').add({'Codi': cd, 'Producte': prd, 'Descripció': dsc, 'Stock': stk, 'Tipus': tps})
                doc_ref = db.collection('Productes').add({'Codi': cd, 'Producte': prd, 'Descripció': dsc, 'Ambit': amb, 'Stock': stk})
                st.write("Actualització realitzada amb èxit")
                st.dataframe(df) 
                



