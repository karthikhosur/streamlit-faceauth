import requests
import streamlit as st
import os
from PIL import Image

directory = 'face'
if not os.path.exists(directory):
    os.makedirs(directory)


def main():
    st.title('Face Verification App')

    page = st.sidebar.selectbox('Choose a page', [
                                'Tutorial', 'Page 1 - Capture Image', 'Page 2 - Verify Image', 'Page 3 - View Saved Image'])

    if page == 'Tutorial':
        st.markdown(
            """
            ## Tutorial

            Welcome to our Face Verification App. This app allows you to store images of individuals and then verify their identity by comparing a new picture with the saved one.

            ### Steps to use this application:

            1. **Capture Image:**
                - Select 'Page 1 - Capture Image' from the sidebar.
                - Enter the person's name.
                - Click the 'Take a picture' button to capture an image.
                - Click 'Save Image' to save the image for this person.

            2. **Verify Image:**
                - Select 'Page 2 - Verify Image' from the sidebar.
                - Enter the person's name for which you want to verify a new image.
                - Click the 'Take a picture for verification' button to capture a new image.
                - Click 'Verify Image' to compare the new image with the stored one. 

            3. **View Saved Image:**
                - Select 'Page 3 - View Saved Image' from the sidebar.
                - Enter the person's name for which you want to see the saved image.
                - Click 'Show Image' to view the saved image.

            The application will return the results of the face verification process, indicating whether the images match.

            Enjoy the app!
            """
        )

    elif page == 'Page 1 - Capture Image':
        name = st.text_input('Enter a person\'s name')
        picture = st.camera_input('Take a picture')
        # Check that 'name' is not empty
        if name and picture and st.button('Save Image'):
            img_path = os.path.join(
                'face', f'{name}.png')
            with open(img_path, "wb") as f:
                f.write(picture.read())
            st.success(f'Image of {name} saved successfully!')

    elif page == 'Page 2 - Verify Image':
        name = st.text_input('Enter the person\'s name to verify')
        picture = st.camera_input('Take a picture for verification')
        # Check that 'name' is not empty
        if name and picture and st.button('Verify Image'):
            new_img_path = os.path.join(
                'face', 'temp.png')
            with open(new_img_path, "wb") as f:
                f.write(picture.read())

            # Verify with stored image
            url = "http://157.230.238.180/verify/images"
            with open(os.path.join('face', f'{name}.png'), 'rb') as old_image:
                files = {
                    'source_image': ('source_image', old_image, 'application/octet-stream'),
                    'target_image': ('target_image', open(new_img_path, 'rb'), 'application/octet-stream')
                }
                headers = {'accept': 'application/json'}
                response = requests.request(
                    "POST", url, headers=headers, files=files)
                st.write(response.json())

    elif page == 'Page 3 - View Saved Image':
        name = st.text_input(
            'Enter the person\'s name to view saved image')
        if name and st.button('Show Image'):
            img_path = os.path.join(
                'face', f'{name}.png')
            try:
                image = Image.open(img_path)
                st.image(image, caption=f'Saved image of {name}')
            except FileNotFoundError:
                st.error(f"No saved image for {name} found!")


if __name__ == "__main__":
    main()
