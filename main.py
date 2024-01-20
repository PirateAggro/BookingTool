import streamlit as st
from streamlit_option_menu import option_menu

import app, reserva_fb, retorn, historial, dadesmestres, materials, reserva_fb_Boot

st.set_page_config(
    page_title="Gestió Reserves",
)


class Multiapp:
    def __ini__(self):
        self.apps = []
    def add_app(self,title,funcion):
        self.apps.append({
            "title": title,
            "function": function
        })
    def run():
        with st.sidebar:
            app = option_menu(
                menu_title='Menu',
                options=["Reserva", "Retorn", "Historial", "Dades Mestres", "Materials","Boot"],
                menu_icon="cast",
                default_index=0
            )
        ##my_expander = st.expander(label='Expand me')
        ##my_expander.write('Hello there!')
        ##clicked = my_expander.button('Click me!')
        
        if app=='Reserva':
            reserva_fb.app()
        if app=='Retorn':
            retorn.app()
        if app=='Historial':
            historial.app()
        if app=='Dades':
            dadesmestres.app()
        if app=='Materials':
            materials.app()
        if app=='Boot':
            reserva_fb_Boot.app()
        

       
    
    run()