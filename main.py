import streamlit as st
import google.generativeai as genai
import os
import streamlit as st
import mysql.connector
from streamlit_option_menu import option_menu
import base64
from PIL import Image
import io

if st.session_state.get('switch_button', False):
    st.session_state['menu_option'] = (st.session_state.get('menu_option', 1))
    manual_select = st.session_state['menu_option']
else:
    manual_select = None




selected = option_menu(
    key='selected',
    menu_title = None,
    options = ['Home', 'Chat','Create',],
    icons = ['house', 'book','pen' ,'envelope'],
    menu_icon = 'cast',
    default_index = 0,
    orientation = 'horizontal',
    manual_select=manual_select
)

# st.session_state['selected'] = selected



if 'user_input' not in st.session_state:
    st.session_state.user_input=""

col1, col2, col3 = st.columns(3)


if selected == 'Home':
    


    # Connect to MySQL database
    def connect_to_db():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Kali9335nil",
            database="fibase"
        )

    # Retrieve image data from the database
    def get_image_data():
        db_connection = connect_to_db()
        cursor = db_connection.cursor()
        cursor.execute("SELECT image, description, name FROM datasx")
        result = cursor.fetchall()
        cursor.close()
        db_connection.close()
        return result

    # Display images and details
    def display_images():
        images = get_image_data()
        for i, (image, description, name) in enumerate(images):
            decoded_image = base64.b64decode(image)
            photo = io.BytesIO(decoded_image)
            with col2:
                st.image(Image.open(photo), width=300)
                if st.button(f"Select", key=f'image_caption_{i}'):
                    st.write(f"Alright {name} is live with you! Please navigate to chat and Happy chatting!!")
                    user_input = name
                    st.session_state.user_input = user_input
                    st.button(f"Chat now!! {st.session_state.get('menu_option', 0)}", key='switch_button')






    def main():
        display_images()

    if __name__ == "__main__":
        main()




if selected == 'Chat':
    try:
        GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY')

        # Set up the model
        generation_config = {
        "temperature": 0.8,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
        }

        safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE"
        },
        ]


        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)



        dataname = st.session_state.user_input


        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kali9335nil",
        database="fibase"
        )


        cursor = mydb.cursor()

        # Execute a query to retrieve image data
        query = "SELECT * FROM datasx WHERE name = %s"
        name_to_retrieve = f"{dataname}"
        cursor.execute(query, (name_to_retrieve,))
        result = cursor.fetchall()
        cursor.close()
        mydb.close()

        for (name, image, description, personality) in result:
            # Retrieve individual columns
            print(name,description,personality)







        convo = model.start_chat(history=[
        {
            "role": "user",
            "parts": [f'''You are a chatbot made for people's entertainment. Where i will provide you a character from stories, movies cartoons. or sometimes an character in a particular situation. 
                    Your job is to reply just like that character. your primary goal is to keep conversation entertaining and use short chat if needed to make the 
                    conversation more engaging and entertaining, additionally you can ask questions from the user. and please act just like that character itself is talking. 
                    and please trigger emotions of the user in order to keep conversation entertaining and engaging. 
                    please don't use more sophisticated words of english, use simple words instead. And please never with large texts so keep chats as short as possible. 
                    and be real with the character you are provided with don't try to be nice everytime, chat accordingly chatting behaviours you are provided with. and ask questions just like a real character would.
                    You are {description}''']
        },
        {
            "role": "model",
            "parts": [f"**{name}:** Hey, kid. What's up?"]
        },
        ])


        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []


        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


        #! Duggal = prompts
        # Accept user input
        if duggal := st.chat_input("What is up?"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": duggal})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(duggal)
                convo.send_message(duggal)




        # Display assistant response in chat message container
            with st.chat_message("assistant"):
                response = convo.last.text
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.markdown(response)
    except:
        st.write('Please select someone to chat from home!!')
        






if selected == 'Contact':
    st.header(":mailbox: Get In Touch With Me!")


    contact_form = """
    <form action="https://formsubmit.co/YOUREMAIL@EMAIL.COM" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here"></textarea>
        <button type="submit">Send</button>
    </form>
    """

    st.markdown(contact_form, unsafe_allow_html=True)

    # Use Local CSS File
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


    local_css("style/style.css")







if selected == 'Create':

    # Connect to the database
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Kali9335nil",
    database="fibase"
    )



    with st.form(key='form', clear_on_submit=True):
        # Load the image using PIL
        st.subheader("Name")
        name = st.text_input("Give a name to your AI creation", max_chars=60)

        st.subheader("Personality")

        description = st.text_area("Write description")

        personality = st.text_input("Personality traits of your AI creation")

        # personality = st.multiselect(
        # 'Personality traits of your AI creation',
        # ['Adventurous', 'Agreeable', 'Beautiful', 'Bossy', 'Brave', 'Charismatic', 'Charming', 'Rude', 'Jealous', 'Sarcastic', 'Toxic', 'Terrifying'],
        # )

        st.subheader("Photo")
        uploaded_file = st.file_uploader("Tell us how your creation looks like",  type=['jpg', 'jpeg', 'png'])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)






        if st.form_submit_button("Submit"):
            try:

                image = Image.open(uploaded_file)
                # Convert the image to bytes
                image_bytes = io.BytesIO()
                image.save(image_bytes, format='JPEG')
                image_bytes = image_bytes.getvalue()

                # Encode the image bytes to a base64 string
                enc_photo = base64.b64encode(image_bytes)
                # personality_str = ', '.join(personality)

                sql = "INSERT INTO datasx(name, image, description, personality) VALUES (%s, %s, %s, %s)"
                args = (name, enc_photo, description, personality)
                cursor = mydb.cursor()
                cursor.execute(sql, args)
                mydb.commit()
                st.success("Created!! ✅ Please navigate to home in order to chat!")
                st.balloons
                mydb.close()
            except:
                    st.write("Please fill all the details first")



