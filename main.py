"""
Usage:
 
streamlit run streamlit_demo.py --server.maxUploadSize=2056

"""
import streamlit as st
from src.summarizeEngine import SummarizeEngine
import pandas as pd
from os import listdir
from os.path import isfile, join
import time



@st.cache_resource
def loadEngine():
    engine = SummarizeEngine()
    return engine

@st.cache_resource
def page():
    st.write('<style>body { margin: 0; font-family: Arial, Helvetica, sans-serif;} \
                .sticky { position: fixed; top: 0; width: 100%;} \
                </style><div class="header" id="myHeader"> <font size="+5"> <b>' + str(
        'Video Summarize. Choose the film') + '</b> </font></div>', \
                unsafe_allow_html=True)
    st.sidebar.image("img/logo.png")

def load_stats():
    st.sidebar.text('Demo based on the summarize \nof content in movies')

    mypath = 'examples'
    onlyfiles = [(f.replace('.mp4', ' ') and f.replace('_', ' ')) for f in listdir(mypath) if isfile(join(mypath, f))]
    count = len(onlyfiles)

    st.sidebar.text('Total available movies: {}'.format(
        count
    ))

    st.sidebar.selectbox("Available movies", onlyfiles)
    with st.spinner('Subiendo video...'):
        uploaded_file = st.file_uploader("Subir video", type=["mp4"])

    if uploaded_file is not None:
        with st.spinner('Generando Trailer...'):
            #st.write('<div class="header" id="myHeader"> <font size="+5"> <b>' + str('Película') + '</b> </font></div>', unsafe_allow_html=True)
           # st.video(uploaded_file)
            time.sleep(10)
            video_name=uploaded_file.name[:-4]
            prueba_video_path = 'trailers/'+video_name+'_trailer_v2.mp4'
            st.write('<div class="header" id="myHeader"> <font size="+5"> <b>' + str('Trailer generado exitosamente') + '</b> </font></div>', unsafe_allow_html=True)
            prueba_video_file = open(prueba_video_path, 'rb')
            prueba_video_bytes = prueba_video_file.read()
            st.video(prueba_video_bytes)


def upload_video():
    st.sidebar.text('Demo basada en el resumen de contenido en películas')

    mypath = 'examples'
    onlyfiles = [(f.replace('.mp4', '') and f.replace('_', ' ')) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    count = len(onlyfiles)

    st.sidebar.text('Películas disponibles: {}'.format(count))

    selected_movie = st.sidebar.selectbox("Películas disponibles", onlyfiles)

    st.text_input("Nombre del video a subir:")
    uploaded_file = st.file_uploader("Subir video", type=["mp4"])

    if uploaded_file is not None:
        # Puedes realizar operaciones adicionales con el archivo cargado
        st.video(uploaded_file)
        

if __name__ == '__main__':
    check_password = True
    if check_password:
        st.set_page_config(  # Alternate names: setup_page, page, layout
            layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
            initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
            page_title='AI Suite: summarize system',
            # String or None. Strings get appended with "• Streamlit".
            page_icon='img/fav_icon_1.png',  # String, anything supported by st.image, or None.
        )
        page()
        load_stats()
        engine = loadEngine()
     
   

            # st.text('BEST MOVIES FOUND')
            # st.dataframe(df_movies)

            # st.text('BEST SCENES FOUND')
            # st.dataframe(df_scenes)


