# Written for First Robotics Team 7613 Sinagua robotics by Mentor Paul Doose
# To assists with camera calibration
#
# Uses openCV to detect a ChArUco board which can then be used to generate
#  camera calibration values.

import cv2
import cv2.aruco as aruco
import numpy as np
import sys
import operator

# Commands to execute when keypresses are detected. (Maps keys to command functions)
commands = {
    # exit program
    ord('q'): operator.methodcaller('exit'), # Call exit function if 'q' or 'x' pressed
    ord('x'): operator.methodcaller('exit'),
    # "add" image to calibration set if board is detected
    ord('a'): operator.methodcaller('add_image'), # call add image if 'a' or 's' pressed
    ord('s'): operator.methodcaller('add_image'),
    # Generates calibration data
    ord('c'): operator.methodcaller('calibrate') # call calibrate if 'c' is pressed
}

class Get_Vid:
    shape = (None,None)

    # initilize
    def __init__(self, cap_device = 0, width=None, height=None):

        # if running windows use Direct Show optimizations else run normally
        if sys.platform == 'win32':
            self.cap = cv2.VideoCapture(0, CAP_DSHOW)
        else:
            self.cap = cv2.VideoCapture(0)

        # open capture device
        self.cap_device = cap_device
        if not self.cap.isOpened():
            raise AttributeError(f"Error: Could not open {self.cap_device}")
        
        # check that paramiters are valid.
        shape = (width, height)
        if width is not None:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        if height is not None:
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    # Read next frame
    def read(self):
        ret, frame = self.cap.read()
        if not ret: # handle any errors
            raise AttributeError(f"Error: Could not read {self.cap_device}")
        return frame
    
    # Release all object to ensure they are properly closed
    def release(self):
        if (self.cap.isOpened()):
            self.cap.release()
    
    # Class destructor, ensureing everything is properly released.
    def __del__(self):
        self.release()

class ChArUco_board:
    # Initilize variables to be used
    aruco_dict = None
    board = None
    
    catch = False
    all_corners = []
    all_ids = []
    im_size = None

    #initilize
    def __init__(self, x, y, square_len = 0.04, marker_len = 0.02, dict = aruco.DICT_5X5_250):
        self.x = x # Number of squares in x direction
        self.y = y # Number of squares in y direction
        self.square_len = square_len  # Length in meters of grid squares
        self.marker_len = marker_len # Length in meters of Arcuo Markers
        if (self.square_len <= self.marker_len): # Verify value range
            raise ValueError("Range Error: marker_len must be smaller than square_len.") 
        self.dict = aruco.DICT_5X5_250
        self.GererateBoard()

    #Generate Board (placed here to allow recreation)
    def GererateBoard(self):
        if (self.dict == None): # Check if board type has been set
            raise ValueError("Type not set")

        self.aruco_dict = aruco.getPredefinedDictionary(self.dict) # Set Arcuo marker type
        self.board = aruco.CharucoBoard((self.x,self.y), self.square_len, self.marker_len, self.aruco_dict)

    # Detect can capture if self.catch flag is set
    def Detect(self, image):
        image_dr = image.copy()
        detector = aruco.CharucoDetector(self.board)

        # Detect paterin in image
        charuco_corners, charuco_ids, marker_corners, marker_ids = detector.detectBoard(image)

        charuco_color = (255, 0, 0)
        marker_color = (0, 0, 255)
        if charuco_corners is not None and charuco_ids is not None:
            cv2.aruco.drawDetectedCornersCharuco(image_dr, charuco_corners, charuco_ids, charuco_color)
        if marker_corners is not None and marker_ids is not None:
            cv2.aruco.drawDetectedMarkers(image_dr, marker_corners, marker_ids, marker_color)

        if self.catch:
            self.catch = False
            self.im_size = image.shape[:2]     

            if (marker_ids is not None) and (len(marker_ids) >= 4):
                self.all_corners.append(charuco_corners)
                self.all_ids.append(charuco_ids)

            print(f"capture: {len(self.all_ids)}, ({self.im_size[1]},{self.im_size[0]})")

        return image_dr
    
    def add_image(self):
        self.catch = True
        return 1 # Used to determine if keypress was processed

    # use captured data to 
    def calibrate(self):
        if (len(self.all_ids) < 5 or self.im_size == None):
            print("Not enough data to generate calibration data.")
            return 0  # Used to determine if keypress was processed

        camera_matrix_init = np.array([[1000.,    0., self.im_size[0]/2.],
                                       [   0., 1000., self.im_size[1]/2.],
                                       [   0.,    0.,                 1.]])
        dist_coeffs_init = np.zeros((5,1))
        flags = (cv2.CALIB_USE_INTRINSIC_GUESS + cv2.CALIB_RATIONAL_MODEL + cv2.CALIB_FIX_ASPECT_RATIO)
        #flags = cv2.CALIB_RATIONAL_MODEL
        (ret, camera_matrix, dist_coeffs,
         rotation_vectors, translation_vectors) = aruco.calibrateCameraCharuco(self.all_corners, self.all_ids, self.board, self.im_size, None, None)
        #print("Camera Matrix:\n", camera_matrix)
        #print("Distortion Matrix:\n", distortion_coefficients)
        #print("Reprojection Error:\n", ret)
        print(f"#''' Camera settings:")
        print(f"resoultion =  ({self.im_size[1]},{self.im_size[0]})")
        print(f"camera_params = ({camera_matrix[0][0]}, {camera_matrix[1][1]}, {camera_matrix[0][2]}, {camera_matrix[1][2]})")
        print(f"dist_coeffs = ({dist_coeffs[0][0]}, {dist_coeffs[0][1]}, {dist_coeffs[0][2]}, {dist_coeffs[0][3]}, {dist_coeffs[0][4]})")
        print(f"#Reprojection Error = {ret}")
        print("#'''")
        return 1  # Used to determine if keypress was processed
    
    def exit(self):
        return -1  # Used to determine if keypress was processed
    

cam = Get_Vid()
board = ChArUco_board(8,6, 1.25 * 0.0254, 1 * 0.0254) # board is 8x6 with 1.25in divisions, and 1in markers using default marker type. (multiply by 0.0254 to convert meters to inches)

while True:
    image = cam.read()
    image = board.Detect(image)

    cv2.imshow("Detection", image)

    key = cv2.waitKey(1) & 0xFF # Get any keypress
    call = commands.get(key, None) # Lookup what function to call with that keypress
    result = call(board) if (call != None) else 0 # call that function and store result, else return 0

    # if result is less than 0 then exit the program by breaking main loop
    if (result < 0):
        break

# cleanup any remaining data before exit
cam.release()
cv2.destroyAllWindows()

       

    