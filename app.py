import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode, RTCConfiguration
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

# RTC configuration
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# Streamlit-webrtc component with RTC configuration
webrtc_ctx = webrtc_streamer(
    key="WYH",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": True, "audio": False},
    video_processor_factory=VideoProcessor,
    async_processing=False,
)
