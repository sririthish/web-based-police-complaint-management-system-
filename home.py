import streamlit as st
from streamlit_option_menu import option_menu
import datetime
import id
import pandas as pd
from pathlib import Path
import os
from csv import writer
from PIL import Image


st.set_page_config(page_title="Crime portal",
                   page_icon=":blossom:", layout="wide")


# def add_bg_from_url():
#     st.markdown(
#         f"""
#          <style>
#          .stApp {{
#              background-image: url("");
#              background-attachment: fixed;
#              background-size: cover
#          }}
#          </style>
#          """,
#         unsafe_allow_html=True
#     )


# add_bg_from_url()

selected2 = option_menu(None, ["Home", "Register a complaint", 'Complaint history', "Complaint status"],
                        icons=['house', 'cloud-upload',
                               "list-task", 'info-circle-fill'],
                        menu_icon="cast", default_index=0, orientation="horizontal")

# try:
user_id = st.session_state["user_id"]
l = []

# st.write(user_id)
if selected2 == "Home":

    st.markdown(
        "<h1 style='text-align: center; color: red;'>Crime Portal</h1>", unsafe_allow_html=True)
    image = Image.open('assets\law.jpg')
    # st.image(image, caption='Sunrise by the mountains')
    col1, col2, col3 = st.columns([0.2, 5, 0.2])
    col2.image(image, width=1138)
    st.write('Government')
    ######

if selected2 == 'Register a complaint':
    st.write('''# Welcome {0}!'''.format(user_id))
    st.markdown(
        "<h1 style='text-align: center; color: #00adff;'>Complaint Register</h1>", unsafe_allow_html=True)
    aadhar = st.text_input(
        "Aadhar", placeholder='Enter your Aadhar number')
    type_crime = st.selectbox('Select the Type of crime', ('Theft', 'Kidnapping', 'Robbery', 'smuggling', 'terrorism', 'Arson', 'Assault and battery', 'bribery', 'burglary', 'child abuse', 'counterfeiting', 'cybercrime', 'drug use', 'embezzlement',
                                'extortion', 'forgery', 'fraud', 'hijacking', 'homicide', 'incest', 'larceny', 'organized crime', 'perjury', 'piracy', 'prostitution', 'rape', 'sedition', 'treason', 'usury'))
    location = st.selectbox(
        'Select the Location of crime',
        ('Ramapuram', 'Manapakkam', 'Adambakkam', 'Alandur', 'Alapakkam', 'Alwarpet', 'Alwarthirunagar', 'Ambattur', 'Aminjikarai', 'Anna Nagar', 'Arumbakkam', 'Ashok Nagar', 'Avadi', 'Mugalivakkam', 'Nesapakkam', 'Porur', 'Padi', 'Sowcarpet', 'St.Thomas Mount', 'Surapet', 'Tambaram', 'Teynampet', 'Tharamani', 'T.Nagar', 'Vandalur', 'Vadapalani', 'Valasaravakkam', 'Vallalar Nagar', 'Vanagaram', 'Velachery'))
    ph_no = st.text_input(
        "phone number", placeholder='Enter your phone number')
    date = st.date_input(
        "Select the Date of crime happened",
        datetime.date(2022, 12, 6))
    # description = st.text_input(
    #     "Description", placeholder='Describe the incident')
    description = st.text_area("Description")

    note_txt = st.text_area(
        'Note', '''If you have a suspicious person, then upload the image of that person, inorder to investigate them.⚠️Warning, The photo you're uploading must not violate our rules and regulation. If it cross our rules the actions would take place!''')

    image_file = st.file_uploader(
        "Upload an image", type=['png', 'jpeg', 'jpg'])
    if st.button('Submit') == True:
        random_id = id.random_sample(5, 1000, 30000)
        st.session_state['temp'] = random_id[0]

        l = [[random_id[0], aadhar, type_crime,
                location, ph_no, date, description]]
        df = pd.DataFrame(l, columns=[
                            'complaint_id', 'aadhar_id', 'type_of_crime', 'location', 'ph_no', 'date', 'description'])

        ############################################################
        # path = 'complaints\{0}_complaint'.format(user_id)
        # temp = os.path.isfile(path)
        # if temp:
        # with open('complaints/{0}_complaint.csv'.format(user_id), 'a') as f_object:
        #     writer_object = writer(f_object)
        #     writer_object.writerow(l)
        #     f_object.close()
        # else:
        #     file_path = Path(
        #         'complaints/{0}_complaint.csv'.format(user_id))
        # df.to_csv(file_path, index=False)
        # print(df)
        ##############################################################
        output_path = 'complaints/{0}_complaint.csv'.format(user_id)
        # df.to_csv(output_path, mode='a', index=False,
        #             header=not os.path.exists(output_path))
        df.to_csv(
            'complaints/{0}_complaint.csv'.format(user_id), mode='a', index=False, header=False)
    # note_txt = st.text_area(
    #     'Note', '''If you have a suspicious person, then upload the image of that person, inorder to investigate them.⚠️Warning, The photo you're uploading must not violate our rules and regulation. If it cross our rules the actions would take place!''')

    # image_file = st.file_uploader(
    #     "Upload an image", type=['png', 'jpeg', 'jpg'])

    if image_file is not None:
        file_details = {"FileName": image_file.name,
                        "FileType": image_file.type}
        st.write(file_details)
        # img = load_image(image_file)
        # st.image(img, height=250, width=250)
        temp = st.session_state['temp']
        with open(os.path.join("suspicious_img", '{0}.jpg'.format(temp)), "wb") as f:
            f.write(image_file.getbuffer())
            st.success("Saved File")

if selected2 == 'Complaint history':
    st.markdown(
        "<h1 style='text-align: center; color: #00adff;'>Complaint History</h1>", unsafe_allow_html=True)
    try:
        df1 = pd.read_csv('complaints/{0}_complaint.csv'.format(user_id))
        st.table(df1)
    except FileNotFoundError:
        st.subheader("You don't have any complaints yet!🙂")

if selected2 == "Complaint status":
    df3 = pd.read_csv('complaints/{0}_complaint.csv'.format(user_id))
    try:
        comp_id = st.selectbox(
            'Select the complaint id', df3['complaint_id'])
        df4 = pd.read_csv(
            'admin_controls/complaint_update/{0}_complaint.csv'.format(comp_id))
        st.table(df4)

    except FileNotFoundError as e:
        st.markdown('''# ⚠️No updates yet!''')


# except FileNotFoundError as e:
#     st.title("404 error")
#     st.subheader("Oops something went wrong...")
#     st.subheader("login agian!")
