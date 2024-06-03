import cv2

import cv2.aruco as aruco


def find_aruco_markers(frame, draw=True):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_100)
    parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dict, parameters)

    corners, ids, rejectedImgPoints = detector.detectMarkers(frame)

    if draw:
        frame = aruco.drawDetectedMarkers(frame, corners, ids)

    return frame, corners, ids, rejectedImgPoints


def main():
    capture = cv2.VideoCapture(0)

    while True:
        ret, frame = capture.read()
        find_aruco_markers(frame)

        cv2.imshow('frame', frame)

        cv2.waitKey(1)

if __name__ == '__main__':
    main()