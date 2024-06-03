import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

st.title("WebRTC Camera Stream with Streamlit")

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# Using WebRTC to stream video from the camera
webrtc_ctx = webrtc_streamer(
    key="WYH",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=False,
)

if webrtc_ctx.video_receiver:
    while True:
        frame = webrtc_ctx.video_receiver.get_frame()
        st.image(frame.to_ndarray(format="bgr24"), channels="BGR")
else:
    st.write("Click the button to start the camera.")
