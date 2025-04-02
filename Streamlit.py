import streamlit as st

st.title("Car Body identification")
st.markdown(
    """ 
    This application harnesses the power of artificial intelligence
    to precisely determine the type of car body in your uploaded photo.
    """
)

a = st.file_uploader("Upload car picture here", type=["jpg", "jpeg", "png"], accept_multiple_files=False)

if a:
    if not (a.name.endswith(".jpg") or a.name.endswith(".png") or a.name.endswith(".jpeg")):
        st.markdown(
            """ 
            It's not .jpg or .png or .jpeg, file 
            """
        )

if st.button("Identify!"):
    if a is not None:
        st.markdown(
            """ 
            This feature will be added shortly 😊
            :rainbow[Be patient!] 😁
            """
        )
        st.balloons()
    else:
        st.markdown(
            """ 
            Upload a file first!
            """
        )
