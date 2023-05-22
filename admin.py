import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import database as db
import os
import identifier
from PIL import Image
import numpy as np

st.set_page_config(page_title='Police',
                   page_icon='assets/favicon.ico', layout='wide')


selected = option_menu(None, ["Home", "pending complaints", 'completed complaint'],
                       icons=['house',
                              "list-task", 'info-circle-fill'],
                       menu_icon="cast", default_index=0, orientation="horizontal")
users = db.fetch_all_users()
names = [user["name"] for user in users]

if selected == "Home":
    st.title('Complaint portal')
    image1 = Image.open('../assets/download.jpeg')
    col1, col2, col3 = st.columns([0.2, 5, 0.2])
    col2.image(image1, width=950)
    import requests
    import json

    url = 'http://api.quotable.io/random'
    if st.button("get some motivation in work!"):
        with st.container():
            col1, col2 = st.columns(2)
            n = np.random.randint(1, 1000, 1)[0]
            with col1:
                quotes = {"Good job and almost done": "checker1",
                          "Great start!!": "checker2",
                          "Please make corrections base on the following observation": "checker3",
                          "DO NOT train with test data": "folk wisdom",
                          "good work, but no docstrings": "checker4",
                          "Well done!": "checker3",
                          "For the sake of reproducibility, I recommend setting the random seed": "checker1"}
                if n % 5 == 0:
                    a = np.random.choice(list(quotes.keys()), 1)[0]
                    quote, author = a, quotes[a]
                else:
                    try:
                        r = requests.get(url=url)
                        text = json.loads(r.text)
                        quote, author = text['content'], text['author']
                    except Exception as e:
                        a = np.random.choice(list(quotes.keys()), 1)[0]
                        quote, author = a, quotes[a]
                    st.markdown(f"## *{quote}*")
                    st.markdown(f"### ***{author}***")
                with col2:
                    st.image(
                        image=f"https://picsum.photos/800/600?random={n}")

if selected == "pending complaints":

    select_user = st.selectbox('Client', names)
    try:

        df = pd.read_csv('../complaints/{0}_complaint.csv'.format(select_user))
        comp_id = st.selectbox('Select the complaint id', df['complaint_id'])
        st.session_state['c'] = comp_id
        df1 = df.loc[df['complaint_id'] == comp_id]
        st.table(df1)
        police_id = st.text_input(
            'Case update', placeholder="Enter the complaint status")

        case_up = [[comp_id, police_id]]
        df3 = pd.DataFrame(case_up, columns=[
                           'complaint_id', 'complaint_progress'])
        st.table(df3)

        if st.button('Update') == True:
            output_path = 'complaint_update/{0}_complaint.csv'.format(comp_id)
            df3.to_csv(output_path, mode='a', index=False,
                       header=not os.path.exists(output_path))

        if st.button("Marked as completed") == True:
            output_path = 'completed_complaint/completed_complaint.csv'
            df1.to_csv(output_path, mode='a', index=False,
                       header=not os.path.exists(output_path))

    except FileNotFoundError as e:
        st.markdown('''# ⚠️No complaints yet!''')

    if st.button('Check for the Suspicious person') == True:
        # st.write(comp_id)
        c = st.session_state['c']
        susp_pers = identifier.face_recogonizer(c)
        df8 = pd.read_csv('aadhar_database/aadhar_details.csv')
        # print(susp_pers)
        df9 = df8.loc[df8['name'] == susp_pers]
        x = df9.index

        for i in x:
            x = i
        if susp_pers == -1:
            st.write('no suspicious person available!')

        else:
            st.subheader('Description:')
            image = Image.open('identified images/{0}.jpg'.format(c))
            col1, col2, col3 = st.columns([0.2, 5, 0.2])
            col2.image(image, width=250)
            # st.write(x)
            # to fetch the data's from the different data sources
            name, aadhar, contact, address, criminal = df9._get_value(x, 'name'), df9._get_value(
                x, 'aadhar_id'), df9._get_value(x, 'ph_no'), df9._get_value(x, 'address'), df9._get_value(x, 'criminal history')
            st.write('Name:', name)
            st.write('Aadhar number:', aadhar)
            st.write('Contact number:', contact)
            st.write('address:', address)
            st.write('Criminal records:', criminal)

if selected == "completed complaint":
    df6 = pd.read_csv('completed_complaint/completed_complaint.csv')
    st.table(df6)
