import cv2
import numpy as np

#######open the video file and play it

cam = cv2.VideoCapture('Test Video 01.mp4')

while True:
    left_top_x = 0
    left_top_y = 0
    left_bottom_x = 0
    left_bottom_y = 0
    right_top_x = 0
    right_top_y = 0
    right_bottom_x = 0
    right_bottom_y = 0
    ret, frame = cam.read()
    if ret is False:
        break

    ######### shrink the frame
    width_temp=frame.shape[0]
    height_temp=frame.shape[1]
    tuplu = (int(frame.shape[0]/2), int(frame.shape[1]/6))# width | height
    frame = cv2.resize(frame, tuplu)
    cv2.namedWindow('Original after scaling')  # Create a named window
    cv2.moveWindow('Original after scaling', 50, 200)
    cv2.imshow('Original after scaling', frame)

    #######  make the frame grey

    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.namedWindow('Grayscale')  # Create a named window
    cv2.moveWindow('Grayscale', 390, 30)
    cv2.imshow("Grayscale",frameGray)

   ########  select the road

    upper_left = (int(0.40*tuplu[0]), int(0.77*tuplu[1]))
    upper_right = (int(0.55*tuplu[0]), int(0.77*tuplu[1]))
    lower_left = (0, int(tuplu[1]))
    lower_right = (int(tuplu[0]), int(tuplu[1]))
    trapezoid_bounds = np.array([upper_right,upper_left, lower_left,lower_right], dtype=np.int32)
    trapezoid_frame = np.zeros((tuplu[1], tuplu[0]), dtype=np.uint8)
    cv2.namedWindow('Trapezoid')  # Create a named window
    cv2.moveWindow('Trapezoid', 780, 30)
    cv2.fillConvexPoly(trapezoid_frame, trapezoid_bounds,1)
    cv2.imshow('Trapezoid',trapezoid_frame*255)


    road_frame = frameGray*trapezoid_frame
    cv2.namedWindow('Road')  # Create a named window
    cv2.moveWindow('Road', 1170, 30)
    cv2.imshow('Road', road_frame)


    ########  top down view

    upper_left_screen = (0, 0)
    upper_right_screen = (tuplu[0], 0)
    lower_left_screen = (0, tuplu[1])
    lower_right_screen = (tuplu[0],tuplu[1])

    screen_bounds = np.array([upper_right_screen,upper_left_screen, lower_left_screen,lower_right_screen], dtype=np.float32)
    trapezoid_bounds = np.float32(trapezoid_bounds)
    magic_matrix = cv2.getPerspectiveTransform(trapezoid_bounds, screen_bounds)
    top_down_frame = cv2.warpPerspective(road_frame,magic_matrix,(tuplu[0],tuplu[1]))
    cv2.namedWindow('Top-Down')  # Create a named window
    cv2.moveWindow('Top-Down', 10, 300)
    cv2.imshow("Top-Down", top_down_frame)

    ####### blur the top down

    blur_frame = cv2.blur(top_down_frame, ksize=(5, 5))
    cv2.namedWindow('Blur')  # Create a named window
    cv2.moveWindow('Blur', 390, 300)
    cv2.imshow("Blur", blur_frame)

    ###### egde detection w/ sober

    sobel_vertical = np.float32([[-1, -2, -1],
                                [0, 0, 0],
                                [+1, +2, +1]])
    sobel_horizontal = np.transpose(sobel_vertical)
    frame_as_float_32=np.float32(blur_frame)
    sobel_vertical_frame=cv2.filter2D(frame_as_float_32,-1,sobel_vertical)
    sobel_horizontal_frame=cv2.filter2D(frame_as_float_32,-1,sobel_horizontal)

    # sobel_vertical_frame=cv2.convertScaleAbs(sobel_vertical_frame)
    # cv2.imshow("Vertical",sobel_vertical_frame)
    # sobel_horizontal_frame=cv2.convertScaleAbs(sobel_horizontal_frame)
    # cv2.imshow("Horizontal",sobel_horizontal_frame)

    sobel_result_frame = np.sqrt(sobel_vertical_frame**2+sobel_horizontal_frame**2)
    sobel_result_frame=cv2.convertScaleAbs(sobel_result_frame)
    cv2.namedWindow('Sobel')  # Create a named window
    cv2.moveWindow('Sobel', 780, 300)
    cv2.imshow('Sobel',sobel_result_frame)

    #####  binarize the frame!

    threshold = int(255/2)
    binar_frame=sobel_result_frame.copy()
    for i in range(0, binar_frame.shape[0]):
        for j in range(0, binar_frame.shape[1]):
            if binar_frame[i][j]<threshold:
                binar_frame[i][j]=0
            else:
                binar_frame[i][j]=255

    cv2.namedWindow('Binarized')  # Create a named window
    cv2.moveWindow('Binarized', 1170, 300)
    cv2.imshow('Binarized', binar_frame)

    #######get rid of noise

    binar_copy_frame = binar_frame.copy()
    columns_5_percents=int(tuplu[0]*0.05)
    binar_copy_frame[0:,0:columns_5_percents]=0
    binar_copy_frame[0:,-columns_5_percents:]=0

    #######  Get the coordinates of street markings on each side of the road

    left_slice=binar_copy_frame[0:tuplu[1],0:int(tuplu[0]/2)]
    right_slice=binar_copy_frame[0:tuplu[1],int(tuplu[0]/2):]
    left_slice_array=np.argwhere(left_slice==255)
    right_slice_array=np.argwhere(right_slice==255)

    left_xs=np.array([int(x) for y,x in left_slice_array])
    left_ys=np.array([int(y) for y,x in left_slice_array])
    right_xs=np.array([int(x+int(tuplu[0]/2)) for y,x in right_slice_array])
    right_ys=np.array([int(y) for y,x in right_slice_array])

    ####### find the lines that detect the edge of the lane

    coordonate_left=np.polyfit(left_xs,left_ys, deg=1)
    coordonate_right=np.polyfit(right_xs,right_ys, deg=1 )
    if int((0-coordonate_left[1])/coordonate_left[0]) in range(-10**8,10**8):
        left_top_y=0
        left_top_x=int((0-coordonate_left[1])/coordonate_left[0])
    if int((tuplu[1]-coordonate_left[1])/coordonate_left[0]) in range(-10 ** 8, 10 ** 8):
        left_bottom_y=tuplu[1]
        left_bottom_x=int((tuplu[1]-coordonate_left[1])/coordonate_left[0])
    if int((0-coordonate_right[1])/coordonate_right[0]) in range(-10 ** 8, 10 ** 8):
        right_top_y=0
        right_top_x=int((0-coordonate_right[1])/coordonate_right[0])
    if int((tuplu[1]-coordonate_right[1])/coordonate_right[0]) in range(-10 ** 8, 10 ** 8):
        right_bottom_y=tuplu[1]
        right_bottom_x=int((tuplu[1]-coordonate_right[1])/coordonate_right[0])


    cv2.line(binar_copy_frame, (left_top_x, left_top_y), (left_bottom_x, left_bottom_y), (200, 0, 0), 10)
    cv2.line(binar_copy_frame, (right_top_x, right_top_y), (right_bottom_x, right_bottom_y), (100, 0, 0), 10)
    cv2.namedWindow('Lines')  # Create a named window
    cv2.moveWindow('Lines', 10, 570)
    cv2.imshow('Lines',binar_copy_frame)

    ####### Good visualization

    #left line
    blank_frame=np.zeros((tuplu[1], tuplu[0]), dtype=np.uint8)
    cv2.line(blank_frame, (left_top_x, left_top_y), (left_bottom_x, left_bottom_y), (255, 0, 0), 7)
    magic_matrix_final_left=cv2.getPerspectiveTransform(screen_bounds,trapezoid_bounds)
    top_down_frame_final_left=cv2.warpPerspective(blank_frame,magic_matrix_final_left,(tuplu[0],tuplu[1]))

    left_slice_final = top_down_frame_final_left[0:tuplu[1], 0:int(tuplu[0] / 2)]
    left_slice_array_final = np.argwhere(left_slice_final == 255)

    left_xs_final = np.array([int(x) for y, x in left_slice_array_final])
    left_ys_final = np.array([int(y) for y, x in left_slice_array_final])
    cv2.namedWindow('Left Line')  # Create a named window
    cv2.moveWindow('Left Line', 390, 570)
    cv2.imshow('Left Line', top_down_frame_final_left)

    #right line
    blank_frame_1=np.zeros((tuplu[1], tuplu[0]), dtype=np.uint8)
    cv2.line(blank_frame_1, (right_top_x, right_top_y), (right_bottom_x, right_bottom_y), (255, 0, 0), 7)
    magic_matrix_final_right=cv2.getPerspectiveTransform(screen_bounds,trapezoid_bounds)
    top_down_frame_final_right=cv2.warpPerspective(blank_frame_1,magic_matrix_final_right,(tuplu[0],tuplu[1]))

    right_slice_final = top_down_frame_final_right[0:tuplu[1], int(tuplu[0] / 2):]
    right_slice_array_final = np.argwhere(right_slice_final == 255)
    right_xs_final = np.array([int(x + int(tuplu[0] / 2)) for y, x in right_slice_array_final])
    right_ys_final = np.array([int(y) for y, x in right_slice_array_final])
    cv2.namedWindow('Right Line')  # Create a named window
    cv2.moveWindow('Right Line', 780, 570)
    cv2.imshow('Right Line', top_down_frame_final_right)

    #show final
    frame_copy = frame.copy()
    for i in range(len(left_xs_final)):
        frame_copy[left_ys_final[i]][left_xs_final[i]]=[50, 50, 250]
    for i in range(len(right_xs_final)):
        frame_copy[right_ys_final[i]][right_xs_final[i]] = [50, 250, 50]


    cv2.namedWindow('Final')  # Create a named window
    cv2.moveWindow('Final', 980, 200)
    cv2.imshow('Final', frame_copy)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
