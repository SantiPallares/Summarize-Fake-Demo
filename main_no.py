"""
Usage:

streamlit run streamlit_demo.py --server.maxUploadSize=2056

"""
import streamlit as st
from src.transcriptionEngine import TranscriptionEngine
import pandas as pd
from os import listdir
from os.path import isfile, join



@st.cache_resource
def loadEngine():
    engine = TranscriptionEngine()
    return engine

@st.cache_resource
def page():
    st.write('<style>body { margin: 0; font-family: Arial, Helvetica, sans-serif;} \
                .sticky { position: fixed; top: 0; width: 100%;} \
                </style><div class="header" id="myHeader"> <font size="+5"> <b>' + str(
        'AI Suite > Highlight clips extraction system') + '</b> </font></div>', \
                unsafe_allow_html=True)
    st.sidebar.image("img/logo.png")

def load_stats():
    st.sidebar.text('Demo based on the indexing and \nsearch of content in movies')

    mypath = 'src/lda'
    onlyfiles = [f.replace('.mp4', '') for f in listdir(mypath) if isfile(join(mypath, f))]
    count = len(onlyfiles)

    st.sidebar.text('Total available movies: {}'.format(
        count
    ))

    st.sidebar.selectbox("Available movies", onlyfiles)




def make_search(sentence, engine):
    bestVideos = engine.searchBestVideos(sentence)
    
    for video, score, videoIndex in bestVideos:
        # videos.append(video)
        scene_start, scene_end, scene_text = ([] for i in range(3))
        
        col1, col2 = st.columns(2)
        col1.markdown('<div style="text-align: center">' + video + '</div>', unsafe_allow_html=True)
        col1.text(' ')

        # col1.text(video)
        col1_1, col1_2, col1_3 = col1.columns(3)
        
        # st.text(video)
        try:
            
            col1_2.image('images/Poster movie {}/Image_1.jpg'.format(video), use_column_width=True)
        except:
            col1_2.markdown('<div style="text-align: center"> No image found :( </div>', unsafe_allow_html=True)

        if score > 0.001:
            best_scenes = engine.searchBestScenes(videoIndex)
            for start, end, text, score in best_scenes:
                
                start_seconds = start // 1000
                end_seconds = end // 1000
                # scene_video.append(video)
                scene_start.append('{:02d}:{:02d}:{:02d}'.format(
                    start_seconds // 3600, (start_seconds % 3600) // 60, (start_seconds % 3600) % 60
                ))
                scene_end.append('{:02d}:{:02d}:{:02d}'.format(
                    end_seconds // 3600, (end_seconds % 3600) // 60, (end_seconds % 3600) % 60
                ))
                scene_text.append(text)
        
        # df_scenes_data = {'movie':scene_video,'start timestamp': scene_start, 'end timestamp': scene_end, 'scene text': scene_text}
        df_scenes_data = {'start timestamp': scene_start, 'end timestamp': scene_end, 'scene text': scene_text}

        df_scenes = pd.DataFrame(df_scenes_data)
        _, col2_2, _ = col2.columns(3)

        if df_scenes.empty:
            col2_2.text('Any scene matches with \nyour search in this \nmovie :(')
        else:
            col2_2.text('Best matching scenes')
            col2.dataframe(df_scenes)

        st.write('***')

        
    # df_movies_data = {'movies':videos}
    # df_movies = pd.DataFrame(df_movies_data)

    # df_scenes_data = {'movie':scene_video,'start timestamp': scene_start, 'end timestamp': scene_end, 'scene text': scene_text}
    # df_scenes = pd.DataFrame(df_scenes_data)
    # return df_movies, df_scenes

#def check_password():
#    """Returns `True` if the user had the correct password."""
#
#    def password_entered():
#        """Checks whether a password entered by the user is correct."""
#        if st.session_state["password"] == st.secrets["password"]:
#            st.session_state["password_correct"] = True
#            del st.session_state["password"]  # don't store password
#        else:
#            st.session_state["password_correct"] = False
#
#    if "password_correct" not in st.session_state:
#        # First run, show input for password.
#        st.text_input(
#            "Password", type="password", on_change=password_entered, key="password"
#        )
#        return False
#    elif not st.session_state["password_correct"]:
#        # Password not correct, show input + error.
#        st.text_input(
#            "Password", type="password", on_change=password_entered, key="password"
#        )
#        st.error("😕 Password incorrect")
#        return False
#    else:
#        # Password correct.
#        return True


if __name__ == '__main__':
    check_password = True
    if check_password:
        st.set_page_config(  # Alternate names: setup_page, page, layout
            layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
            initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
            page_title='AI Suite: indexing system',
            # String or None. Strings get appended with "• Streamlit".
            page_icon='img/fav_icon_1.png',  # String, anything supported by st.image, or None.
        )
        page()
        load_stats()
        engine = loadEngine()
        text_input = st.text_input(
        "Enter some text 👇"
        )

        if len(text_input) > 0:
            make_search(text_input, engine)

            # st.text('BEST MOVIES FOUND')
            # st.dataframe(df_movies)

            # st.text('BEST SCENES FOUND')
            # st.dataframe(df_scenes)


