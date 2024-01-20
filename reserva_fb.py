# Install required libraries
# Run these commands in your terminal or command prompt
# pip install streamlit
# pip install gspread
# pip install oauth2client

import streamlit as st
import pandas as pd
import gspread
import firebase_admin
from firebase_admin import firestore
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_option_menu import option_menu
from datetime import datetime, date
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
   
    unique_clients_code = []
    unique_clients_code.append(" ")

    unique_clients_name = []
    unique_clients_name.append(" ")

    unique_products_code = []
    unique_products_code.append(" ")

    reserves_check = ""
    
    ambit = " "
    st.title("Gestió Reserves Material")

    # Enter the published Google Sheet URL
    #sheet_url = st.text_input("Enter Google Sheet URL:")
    
    defaul_option  = ""

    df_clients = db.collection("Clients")
    df_productes = db.collection("Productes")
    df_reserves = db.collection("Reserves")

    counter_clients = 0
    counter_productes = 0
    counter_reserves = 0

    selected_cicle = " "
    selected_data_inici = ""
    selected_data_fi = ""

    for doc in df_clients.stream():
        counter_clients = counter_clients + 1
        ##st.write("The id is: ", doc.id)
        ##st.write("The contents are: ", doc.to_dict().items())

        # for field, value in doc.to_dict().items():
            # if field == 'Alumne':
                # unique_clients_code = {value}.add
                ##st.write(f"Field: {field}, Value: {value}")
        ##        st.write({value})
    
    st.write("Total number of clients is ", counter_clients)
    ##st.write(unique_clients_code)

    for doc in df_productes.stream():
        counter_productes = counter_productes + 1
    
    st.write("Total number of product is ", counter_productes)


    for doc in df_reserves.stream():
        counter_reserves = counter_reserves + 1
    
    st.write("Total number of bookings is ", counter_reserves)



    ##sheet_url = "https://docs.google.com/spreadsheets/d/1uMANAvFf14030QZHner0incZyE2Tj9ex04Uiu1H-ldE/edit#gid=0"
    ##if sheet_url:
    ##    # Read data from the Google Sheet
    ##    df = read_google_sheet(sheet_url)

        # Display the data in Streamlit
    ##    st.dataframe(df)

    ##sheet_url = "https://docs.google.com/spreadsheets/d/10OJjKforD1t0VSG1ynpa5QlQ2WbvmXDCGz8R4yxkoXM/edit#gid=0"
    ##if sheet_url:
        # Read data from the Google Sheet
    ##    df2 = read_google_sheet(sheet_url)

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
            # reservat_per_codi = df_clients['Alumne'].unique()
            for doc in df_clients.stream():
                for field, value in doc.to_dict().items():
                    if field == 'Alumne':
                        unique_clients_code.append(value)
                        ## st.write(f"Field: {field}, Value: {value}")
                        ## st.write({value})
            selected_codi = st.selectbox('Reservat per (codi):', unique_clients_code)
            # Filter rows where the 'Column1' is greater than 10
            st.write("Escollit", selected_codi)
            ##filtered_df = df_clients[df_clients['Alumne']==selected_codi]
            ##ambit = filtered_df['AP'].iloc[0]
            ##selected_nom = filtered_df['Nom'].iloc[0]
            #result_text.text(nom_get)
            
        elif choice == 'Selecció per nom':
            ##reservat_per_nom = df_clients['Nom'].unique()
            for doc in df_clients.stream():
                for field, value in doc.to_dict().items():
                    if field == 'Nom':
                        unique_clients_name.append(value)
                        
            selected_nom = st.selectbox('Reservat per (nom):', unique_clients_name)
            # Filter rows where the 'Column1' is greater than 10
            ##filtered_df = df_clients[df_clients['Nom']==selected_nom]
            ##ambit = filtered_df['AP'].iloc[0]
            ##selected_codi = filtered_df['Codi'].iloc[0]
            st.write("Escollit", selected_nom)
            #st.write(filtered_df['AP'])
        else:
            st.write("Please make a selection.")
        
        if choice == 'Selecció per codi':
            query = db.collection('Clients').where('Alumne', '==', selected_codi)
        else:
            query = db.collection('Clients').where('Nom', '==', selected_nom)
        
        for doc in query.stream():
            for field, value in doc.to_dict().items():
                    if field == 'AP':
                        ambit = value
                    if field == 'Nom':
                        selected_nom = value
                    if field == 'Cicle':
                        selected_cicle = value

        st.write(ambit)
        
        if ambit == "A":
            query_product = db.collection('Productes').where('Ambit', '==', ambit)
            for doc in query_product.stream():
                for field, value in doc.to_dict().items():
                    if field == 'Codi':
                        unique_products_code.append(value)
        elif ambit == "P":
            for doc in df_productes.stream():
                for field, value in doc.to_dict().items():
                    if field == 'Codi':
                        unique_products_code.append(value)

        unique_products_code.sort()
        # Use st.date_input to get a date range input from the user
        start_date = st.date_input('Data Entrega', pd.to_datetime('today') - pd.DateOffset(days=7))
        start_date2 = start_date.strftime('%Y-%m-%d')
        end_date = st.date_input('Data Retorn', pd.to_datetime('today'))
        end_date2 = end_date.strftime('%Y-%m-%d')
        flag_validesa_reserva = True

        # selected_material = st.selectbox('Material a reservar:',unique_products_code)
        selected_material = st.multiselect('Material a reservar: ', unique_products_code)
        for product_code_selected in selected_material:
            if product_code_selected!="":          
                query_product = db.collection('Productes').where('Codi', '==', product_code_selected)
                for doc in query_product.stream():
                    for field, value in doc.to_dict().items():
                        if field == 'Codi':
                            selected_codi = value
                        if field == 'Descripció':
                            selected_descripcio = value
                # Display the selected date range
                st.write(f'Selected Date Range: {start_date} to {end_date}')

                # Define selectable date range
                # start_date = pd.to_datetime(start_date1, format='%d/%m/%Y')
                # end_date = pd.to_datetime(end_date1, format='%d/%m/%Y')

                # check availabilty per material and dates
                # retrieve all entries in Reserves: x material  and estat_entrega = pendent

                flag_check_data = ""
                flag_validesa_reserva = True
                query_check = db.collection('Reserves').where('Material', '==', product_code_selected).where('Estat_entrega', '==', 'pendent')
                for doc in query_check.stream():
                    flag_check_data = "x"
                    for field, value in doc.to_dict().items():
                        if field == 'Data_inici':
                            Data_Inici = value
                            Data_Inici2 = Data_Inici.strftime('%Y-%m-%d')
                            st.write("Data Inici",Data_Inici2)
                        if field == 'Data_fi':
                            Data_Final = value
                            Data_Final2 = Data_Final.strftime('%Y-%m-%d')
                            st.write("Data Final",Data_Final2)
                    if Data_Inici2 <= start_date2 <= Data_Final2 or Data_Inici2 <= end_date2 <= Data_Final2:
                    #st.write("La reserva no és possible.")
                        flag_validesa_reserva = False
                    elif start_date2 <= Data_Inici2 and end_date2 >= Data_Final2:
                        #st.write("La reserva no és possible.")
                        flag_validesa_reserva = False
                    else:
                        #st.write("Reserva ok")
                        flag_validesa_reserva = True
                if flag_check_data == "":
                    st.write('Producte : ', product_code_selected, " NO te reserves prèvies")
                    st.write('Producte : ', product_code_selected, " check is ", flag_validesa_reserva)
                    flag_validesa_reserva = True
                else:
                    st.write('Producte : ', product_code_selected, " SI te reserves prèvies")
                    st.write('Producte : ', product_code_selected, " check is ", flag_validesa_reserva)
                # update Reserves collection with new entry
            
            if flag_validesa_reserva == True:
                submit = st.button("Submit new booking for product ", product_code_selected)            
                if submit:
                
                    df_reserves = db.collection("Reserves").document(selected_codi)
                    result = df_reserves.set({
                        "Client": selected_codi,
                        "Nom": selected_nom,
                        "Ambit": ambit,
                        "Material": product_code_selected,      
                        "Descripció": selected_descripcio,
                        "Data_Reserva": datetime.now(),
                        "Data_inici": pd.to_datetime(start_date, format='%d/%m/%Y'),
                        "Data_fi": pd.to_datetime(end_date, format='%d/%m/%Y'),
                        "Quantitat": 1,
                        "Estat_entrega": "pendent"
                    })
                
                    document_Check =  df_reserves.get()
                    if document_Check.exists:
                        st.write("Data found:", document_Check.to_dict())
                    else:
                        st.write("Data not found")