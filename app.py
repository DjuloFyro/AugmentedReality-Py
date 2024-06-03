import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import cv2
import av
from aruco_detector import find_aruco_markers

st.title("Camera Stream with OpenCV and Streamlit")

class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.camera_active = False

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        # Apply the aruco marker detection
        find_aruco_markers(img)
        
        return av.VideoFrame.from_ndarray(img, format="bgr24")

# Streamlit-webrtc component
ctx = webrtc_streamer(key="sample", video_processor_factory=VideoProcessor)