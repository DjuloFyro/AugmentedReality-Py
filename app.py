import streamlit as st
import cv2
from aruco_detector import find_aruco_markers

st.title("Camera Stream with OpenCV and Streamlit")

# Placeholder for the camera frame
frame_placeholder = st.empty()

# Button to start and stop the camera
if "camera_active" not in st.session_state:
    st.session_state.camera_active = False

if st.button("Toggle Camera"):
    st.session_state.camera_active = not st.session_state.camera_active

if st.session_state.camera_active:
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("Failed to open camera.")
    else:
        while st.session_state.camera_active:
            ret, frame = cap.read()
            find_aruco_markers(frame)
            if not ret:
                st.error("Failed to read frame from camera.")
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(frame)

            # Break the loop if the button is toggled off
            if not st.session_state.camera_active:
                break
        cap.release()

st.write("Click the button to open or end the camera.")