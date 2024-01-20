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
from datetime import datetime, timezone, timedelta, date
from google.cloud import firestore
from itertools import islice

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("firestore-key.json")

def crear_reserva():
    st.write(" HOLA - RESERVA CREADA")

def check_reserva(product_code_selected, start_date2, end_date2):

    start_date2 = start_date2.replace(tzinfo=timezone.utc)
    end_date2 = end_date2.replace(tzinfo=timezone.utc)
    flag_check_data = ""
    flag_validesa_reserva = True
    product_assigned = ""
    query_check = db.collection('Reserves').where('Material', '==', product_code_selected).where('Estat_entrega', '==', 'pendent')
    for doc in query_check.stream():
        flag_check_data = "x"
        for field, value in doc.to_dict().items():
            if field == 'Data_inici':
                Data_Inici = value
                #Data_Inici2 = Data_Inici.strftime('%Y-%m-%d')
                Data_Inici2 = pd.to_datetime(Data_Inici, format='%Y-%m-%d')
                #Data_Inici2 = value
                st.write("Data Inici",Data_Inici2)
                st.write("Start Date", start_date2)

            if field == 'Data_fi':
                Data_Final = value
                #Data_Final2 = Data_Final.strftime('%Y-%m-%d')
                Data_Final2 = pd.to_datetime(Data_Final, format='%Y-%m-%d')
                #Data_Final2 = value
                st.write("Data Final",Data_Final2)
                st.write("End Date", end_date2)

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
        st.write(start_date2)
        st.write('Producte : ', product_code_selected, " check is ", flag_validesa_reserva)
        flag_validesa_reserva = True
    else:
        st.write('Producte : ', product_code_selected, " SI te reserves prèvies")
        st.write('Producte : ', product_code_selected, " check is ", flag_validesa_reserva)

    return flag_validesa_reserva

def card(a,b,c):
    return f"""
      <table>
        <thead>
          <tr>
              <th>Clients</th>
              <th>Products</th>
              <th>Reserves</th>
          </tr>
        </thead>

        <tbody>
          <tr>
            <td>{a}</td>
            <td>{b}</td>
            <td>{c}</td>
          </tr>
        </tbody>
      </table>
    """

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

    unique_products_type = []
    unique_products_type.append(" ")

    reserves_check = ""
    
    ambit = " "
    data = []

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
    
    # st.write("Total number of clients is ", counter_clients)
    
    for doc in df_productes.stream():
        counter_productes = counter_productes + 1
    
    # st.write("Total number of product is ", counter_productes)


    for doc in df_reserves.stream():
        counter_reserves = counter_reserves + 1
    
    # st.write("Total number of bookings is ", counter_reserves)

    st.markdown(card(counter_clients,counter_productes,counter_reserves), unsafe_allow_html=True)


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
        alumne_1 = ""
        nom = ""
        if choice == 'Selecció per codi':
            for doc in df_clients.stream():
                for field, value in doc.to_dict().items():
                    if field == 'Alumne':
                        alumne_1 = value
                    if field == 'Nom':
                        nom = value
                concat = str(alumne_1) + " - "+ nom
                unique_clients_code.append(concat)
            unique_clients_code.sort
            selected_codi = st.selectbox('Reservat per (codi):', unique_clients_code)
            st.write("Escollit", selected_codi)   
            # if selected_codi > 0:
            separator = " - "
            part = selected_codi.split(separator)
            st.write(" Part: ", part)
            st.write(part[0])
            selected_codi = int(part [0])        
            st.write("Escollit codi", selected_codi)  


        elif choice == 'Selecció per nom':
            for doc in df_clients.stream():
                for field, value in doc.to_dict().items():
                    if field == 'Nom':
                        unique_clients_name.append(value)   
            selected_nom = st.selectbox('Reservat per (nom):', unique_clients_name)
            st.write("Escollit", selected_nom)

        else:
            st.write("Please make a selection.")
        
        if choice == 'Selecció per codi':
            query = db.collection('Clients').where('Alumne', '==', selected_codi)
        else:
            query = db.collection('Clients').where('Nom', '==', selected_nom)

        # query segons elecció a radiobutton i selecció        
        for doc in query.stream():
            for field, value in doc.to_dict().items():
                    if field == 'AP':
                        ambit = value
                    if field == 'Nom':
                        selected_nom = value
                    if field == 'Cicle':
                        selected_cicle = value
                    if field == 'Alumne':
                        alumne = value
                    if field == 'Nom':
                        nom_alumne = value

        st.write(ambit)

        unique_products_type = set()
        if ambit == "A":
            query_product = db.collection('Productes').where('Ambit', '==', ambit)
            for doc in query_product.stream():
                for field, value in doc.to_dict().items():
                    if field == 'Codi':
                        unique_products_code.append(value)
                    if field == 'Producte':
                        unique_products_type.add(value)
        elif ambit == "P":
            for doc in df_productes.stream():
                for field, value in doc.to_dict().items():
                    if field == 'Codi':
                        unique_products_code.append(value)
                    if field == 'Producte':
                        unique_products_type.add(value)

        unique_products_code.sort()
        
        # Use st.date_input to get a date range input from the user
        start_date = st.date_input('Data Entrega', pd.to_datetime('today'))
        #start_date2 = start_date.strftime('%Y-%m-%d')
        start_date2 = pd.to_datetime(start_date, format='%Y-%m-%d')
        end_date = st.date_input('Data Retorn', pd.to_datetime('today') + pd.DateOffset(days=7))
        #end_date2 = end_date.strftime('%Y-%m-%d')
        end_date2 = pd.to_datetime(end_date, format='%Y-%m-%d')
        flag_validesa_reserva = True

        # selected_material = st.selectbox('Material a reservar:',unique_products_code)
        producte_assignat = []   # per cada tipus de material, codi assignat.
       
        my_list = []
        my_list_productes = []
        my_list_descripcio = []
        my_list_data_inici = []
        my_list_data_fi = []
        st.write(start_date2)
        selected_type = st.multiselect('Tipus de material a reservar: ', unique_products_type)
        for product_type_selected in selected_type:
            if product_type_selected!="":          
                primer_producte = ""
                query_product = db.collection('Productes').where('Producte', '==', product_type_selected)
                for doc in query_product.stream():
                    for field, value in doc.to_dict().items():
                        if field == 'Codi':
                            selected_product_codi = value
                        if field == 'Descripció':
                            selected_descripcio = value
                    st.write("Type: ",product_type_selected, " Codi: ", selected_product_codi, " Descripció: ", selected_descripcio)
                    
                    
                    
                    if isinstance(start_date2, str):
                        st.write("date_string is a string")
                    else:
                        st.write("date_string is not a string")

                    if isinstance(start_date2, datetime):
                        st.write("date_datetime is a datetime object")
                    else:
                        st.write("date_datetime is not a datetime object")
                    
                    
                    
                    
                    
                    a = check_reserva(selected_product_codi,start_date2,end_date2)
                    if a == True:
                        if primer_producte == "":
                            producte_assignat.append(selected_product_codi)
                            primer_producte = "X"
                            #t = (product_type_selected, selected_product_codi,selected_descripcio, start_date2, end_date2)
                            #my_list.append(t)
                            #st.write(t)
                            my_list_productes.append(selected_product_codi)
                            my_list_descripcio.append(selected_descripcio)
                            my_list_data_inici.append(start_date2)
                            my_list_data_fi.append(end_date2)
        

        colms = st.columns((1,2,2,1,1))
        fields=['Num','Producte','Inici','Final','Acció']
        for col,field_name in zip(colms,fields):
            # header
            col.write(field_name)

        # Combine the lists using zip
        my_list = zip(my_list_productes, my_list_descripcio, my_list_data_inici, my_list_data_fi)
        col1,col2,col3,col4,col5 =st.columns((1,2,2,1,1))
        for index, row in enumerate(my_list, start=1):
            col1.write(row[0])
            col2.write(row[1])
            col3.write(row[2])
            col4.write(row[3])
            button_phold = col5.empty()
            do_action = button_phold.button("a", key=index)
            if do_action:
                    st.write(index)
                    df_reserves = db.collection("Reserves").document()
                    result = df_reserves.set({
                        "Client": alumne,
                        "Nom": nom_alumne,
                        "Ambit": ambit,
                        "Material": row[0],      
                        "Descripció": row[1],
                        "Data_Reserva": datetime.now(),
                        "Data_inici": row[2],
                        "Data_fi": row[3],
                        "Quantitat": 1,
                        "Estat_entrega": "pendent"
                        })
                    document_Check =  df_reserves.get()
                    if document_Check.exists:
                        st.write("Data found:", document_Check.to_dict())
                    else:
                        st.write("Data not found")