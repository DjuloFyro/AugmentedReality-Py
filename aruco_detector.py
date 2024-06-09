import cv2
import numpy as np
import cv2.aruco as aruco


def find_aruco_markers(frame: np.ndarray, draw: bool = True) -> tuple[tuple[np.ndarray, ...], np.ndarray]:
    """
    Find ArUco markers in the frame and draw them if draw is True.

    Args:
        frame: The frame to find the markers in.
        draw: Whether to draw the markers on the frame.
    Returns:
        The frame with the markers drawn on it.
    """
    #img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_100)
    parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dict, parameters)

    corners, ids, rejectedImgPoints = detector.detectMarkers(frame)

    if draw:
        frame = aruco.drawDetectedMarkers(frame, corners, ids)

    return corners, ids


def augment_aruco_markers(frame: np.ndarray, augmented_image: np.ndarray, corners: np.ndarray, id: np.ndarray) -> np.ndarray:
    """
    Augment the ArUco markers in the frame.

    Args:
        frame: The frame to augment the markers in.
        corners: The corners of the markers.
        ids: The ids of the markers.
    Returns:
        The frame with the markers augmented.
    """
    top_left = corners[0][0][0], corners[0][0][1]
    top_right = corners[0][1][0], corners[0][1][1]
    bottom_right = corners[0][2][0], corners[0][2][1]
    bottom_left = corners[0][3][0], corners[0][3][1]

    height, width, rgb = augmented_image.shape

    source_plane = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
    target_plane = np.array([top_left, top_right, bottom_right, bottom_left], dtype=np.float32)

    # Find the homography matrix and warp the augmented image
    homography_matrix, status = cv2.findHomography(source_plane, target_plane, cv2.RANSAC, 5.0)
    augmented_image = cv2.warpPerspective(augmented_image, homography_matrix, (frame.shape[1], frame.shape[0]))

    # Fill the marker with black
    cv2.fillConvexPoly(frame, target_plane.astype(int), 0)

    return augmented_image + frame


def main():
    capture = cv2.VideoCapture(0)

    while True:
        ret, frame = capture.read()
        
        corners, ids = find_aruco_markers(frame)
        
        if ids is None:
            print("No markers found.")
        else:
            for corner, id in zip(corners, ids):
                frame = augment_aruco_markers(frame, cv2.imread("images/flower.jpg"), corner, id)

        cv2.imshow('frame', frame)

        cv2.waitKey(1)

if __name__ == '__main__':
    main()