import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_option_menu import option_menu
from datetime import datetime, timezone, timedelta, date
from google.cloud import firestore
from itertools import islice
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid import GridOptionsBuilder

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

def app():

    st.write("Retorn")

    concat = ""
    unique_clients_code = []
    unique_clients_code.append(" ")

    unique_clients_name = []
    unique_clients_name.append(" ")

    selected_codi = ""
    ambit = ""

    df_clients = db.collection("Clients")

    query = db.collection('Clients').where('AP', '==', "P")
    for doc in query.stream():
        for field, value in doc.to_dict().items():
            if field == 'Alumne':
                alumne_1 = value
            if field == 'Nom':
                nom = value
        concat = str(alumne_1) + " - "+ nom
        unique_clients_code.append(concat)

    unique_clients_code.sort
    selected_codi_docent = st.selectbox('Personal Docent que recepciona material:', unique_clients_code)
    docent = selected_codi_docent
    st.write("Escollit", selected_codi_docent)   
    # if selected_codi > 0:
    separator = " - "
    part = selected_codi_docent.split(separator)
    st.write(" Part: ", part)
    st.write(part[0])
    selected_codi_docent = int(part [0])        
    st.write("Escollit codi", selected_codi_docent)  

    query = db.collection('Clients')
    for doc in query.stream():
        for field, value in doc.to_dict().items():
            if field == 'Alumne':
                alumne_1 = value
            if field == 'Nom':
                nom = value
        concat = str(alumne_1) + " - "+ nom
        unique_clients_code.append(concat)

    unique_clients_code.sort
    selected_codi_reservador = st.selectbox('Codi Alumne/Docent que va reservar material:', unique_clients_code)
    st.write("Escollit", selected_codi_reservador)
    # if selected_codi > 0:
    separator = " - "
    part = selected_codi_reservador.split(separator)
    st.write(" Part: ", part)
    st.write(part[0])
    selected_codi_reservador = int(part [0])        
    st.write("Escollit codi", selected_codi_reservador)  


    df_reserves = db.collection("Reserves")
    query = db.collection('Reserves').where('Client', '==', selected_codi_reservador)

    reserva_id = []
    reserva_material = []
    reserva_client = []
    reserva_nom = []
    reserva_inicial = []
    reserva_final = []
    reserva_estat = []

    # Personal docent que fa la recepció

    for doc in query.stream():
        document = doc.id
        document2 = doc.reference
        for field, value in doc.to_dict().items():
            if field == 'Client':
                client = value
            if field == 'Material':
                material =value
            if field == 'Data_inici':
                inici = value
            if field == 'Data_fi':
                final = value
            if field == 'Nom':
                nom = value
            if field == 'Estat_entrega':
                estat = value
        if estat == "pendent" :
            reserva_id.append(document)
            reserva_material.append(material)
            reserva_client.append(client)
            reserva_nom.append(nom)
            reserva_inicial.append(inici)
            reserva_final.append(final)
            reserva_estat.append(estat)

    new_data = {
    'key': reserva_id,
    'Material': reserva_material,
    'Client': reserva_client,
    'Inici': reserva_inicial,
    'Final': reserva_final
    }

    df = pd.DataFrame(new_data)
    gd = GridOptionsBuilder.from_dataframe(df)
    # gd.configure_pagination(enabled=True)
    # gd.configure_default_column(editable=True, groupable=True)

    # sel_mode = st.radio('Selection Type', options= ['single', 'multiple'])
    sel_mode = 'multiple'
    gd.configure_selection(selection_mode=sel_mode,use_checkbox=True)
    gridoptions = gd.build()
    grid_table = AgGrid(df, gridOptions=gridoptions,
                        update_mode=GridUpdateMode.SELECTION_CHANGED,
                        allow_unsafe_jscode=True,
                        theme = 'alpine')
    # height=500,
    sel_row = grid_table["selected_rows"]
    st.write(sel_row)
    flag_update = ""
    options = ["","Material retornat sense incidències", "Material retornat amb incidències"]
    for row in sel_row:
        selected_option = st.selectbox('Estat del Material:', options)
        if selected_option == "Material retornat amb incidències":
            multiline_text = st.text_area("Comentari Estat Material:", "")
        st.write("Selected Row:")
        if selected_option != "":
            if selected_option == "Material retornat sense incidències":
                flag_update = "x"
            if (selected_option == "Material retornat amb incidències") and (multiline_text != ""):
                flag_update = "x"
            if flag_update == "x":
                for field, value in row.items():
                    if field == "key":
                        st.write(f"{field}: {value}")
                        #df_reserves = db.collection("Reserves")                
                        #query = db.collection("Reserves").where(document, '==', value).limit(1)
                        doc_ref = db.collection("Reserves").document(value)

                        # Get the document data
                        doc_data = doc_ref.get()

                        # Check if the document exists
                        if doc_data.exists:
                            # Update the specific field in the document
                            fields_to_update = {
                                'Estat_entrega': "retornat",
                                'Retornat_a': docent,
                                'Data_Retorn': pd.to_datetime('today'),
                                'Estat_Retorn': selected_option,
                                'Comentari_Retorn': multiline_text
                            }
                            doc_ref.update(fields_to_update)

                            st.write(f"Document {value} updated.")
                        else:
                            st.write(f"Document {value} not found.")
