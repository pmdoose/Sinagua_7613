# Written for First Robotics Team 7613 Sinagua robotics by Mentor Paul Doose
# To assists with camera calibration
#
# Uses openCV to generate a ChArUco board which can be printed and used
#  for camera calibration

import cv2
import cv2.aruco as aruco


class ChArUco_board:
    aruco_dict = None
    board = None

    #initilize
    def __init__(self, x, y, square_len = 0.04, marker_len = 0.02, dict = aruco.DICT_5X5_250):
        self.x = x # Number of squares in x direction
        self.y = y # Number of squares in y direction
        self.square_len = square_len # Length in meters of grid squares
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

    #Generate Board Image
    def GenerateImage(self, px=0, py=0): # px = pixels in x dir, py = pixels in y dir
        if (px==0): # Set Default px
            px = self.x*100
        if (py==0): # Set Default py
            py = self.y*100
        if (self.board == None): # Check if board has been set
            raise ValueError("Board not set")
        
        return self.board.generateImage((px, py))
    

    
board = ChArUco_board(8,6, 1.25 * 0.0254, 1 * 0.0254)
board_img = board.GenerateImage()
#border_type = cv2.BORDER_CONSTANT
#border_color = (255, 255, 255)
#board_img = cv2.copyMakeBorder(board_img, 50,50,50,50, border_type, border_color)
cv2.imwrite("ChArUco_img.png", board_img)
cv2.imshow("ChArUco board", board_img)
cv2.waitKey(0)
cv2.destroyAllWindows()