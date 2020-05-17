from Controls import *
import argparse
from collections import deque
from imutils.video import VideoStream
import imutils
import math
import cv2
import time
import numpy as np

def motionTrack(media, handcolor=((110,50,50), (130,255,255))):
  # initialize
  parser = argparse.ArgumentParser()
  parser.add_argument('-b', '--buffer', default=20, type=int)
  buf = vars(parser.parse_args())

  curr_pts = deque(maxlen=buf['buffer'])
  count, count_2, fingerHold = 0, 0, 0
  dx, dy = 0, 0
  direction = ''

  cam = VideoStream(src=0).start()
  time.sleep(1.0)

  gesture_break = 0

  # loop
  while True:
    frame = cam.read()

    if frame is None:
      break

    hsv = cv2.cvtColor(cv2.GaussianBlur(frame, (15, 15), 0, 0), cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, handcolor[0], handcolor[1])
    
    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    new_pt = None
    oldFingers = 0

    if len(contours) > 10:
      #get new ref pt
      max_curve = max(contours, key=cv2.contourArea)
      mu = cv2.moments(max_curve)
      new_pt = int(mu['m10']/mu['m00']), int(mu['m01']/mu['m00'])

      curr_pts.appendleft(new_pt)
      
      #get fingers
      try:
        oldFingers = fingers
      except:
        pass
      fingers = 0
      contour = cv2.approxPolyDP(max_curve, (0.000001*cv2.arcLength(max_curve,True)),True)
      convex_hull = cv2.convexHull(contour, returnPoints=False)
      convex_defects = cv2.convexityDefects(contour, convex_hull)
      try:
        for defect_i in range(convex_defects.shape[0]):
          #check if depth is not noise
          start, end, depth_point, depth = convex_defects[defect_i,0]
          start, end, depth_point = contour[start][0], contour[end][0], contour[depth_point][0]

          #since we know the vertices, we can make an SSS triangle
          s_1 = math.sqrt( ((start[0]-end[0])**2)+((start[1]-end[1])**2) )
          s_2 = math.sqrt( ((start[0]-depth_point[0])**2)+((start[1]-depth_point[1])**2) )
          s_3 = math.sqrt( ((end[0]-depth_point[0])**2)+((end[1]-depth_point[1])**2) )
          #area of an SSS triangle
          half_perimeter = (s_1+s_2+s_3) / 2
          triangle_area = half_perimeter*(half_perimeter-s_1)*(half_perimeter-s_2)*(half_perimeter-s_3)
          height = (math.sqrt(triangle_area)/s_1)*2
          angle_btw_fingers = (s_2**2 + s_3**2 - s_1**2)/(2*s_2*s_3)
          angle_btw_fingers = math.acos(angle_btw_fingers) * (180/math.pi)
          
          if  angle_btw_fingers > 4 and angle_btw_fingers < 75 and height > 50:
            fingers += 1
            # cv2.line(frame, (int(start[0]),int(start[1])), (int(end[0]),int(end[1])), (0, 0, 255), 1)
            # cv2.line(frame, (int(depth_point[0]),int(depth_point[1])), (int(end[0]),int(end[1])), (0, 0, 255), 1)
            # cv2.line(frame, (int(start[0]),int(start[1])), (int(depth_point[0]),int(depth_point[1])), (0, 0, 255), 1)
            
        fingers += 1
        cv2.putText(frame, str(fingers), (0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3, cv2.LINE_AA)
        if oldFingers == fingers:
          fingerHold += 1
        else:
          fingerHold = 1
      except:
        pass
      
      #get direction
      try:
        if count_2 > 10 and curr_pts[-1] is not None:
          direction_x = ''
          direction_y = ''
          dx, dy = curr_pts[-1][0]-new_pt[0], curr_pts[-1][1]-new_pt[1]
          if abs(dx) > 200:
            direction_x = 'right'
            if np.sign(dx) < 1:
              direction_x = 'left'

          if abs(dy) > 200:
            direction_y = 'up'
            if np.sign(dy) < 1:
              direction_y = 'down'
          
          if direction_x != '' and direction_y != '':
            direction = ''
          elif direction_x != '':
            direction = direction_x
          else:
            direction = direction_y
      except:
        pass

      count += 1
      if media == 'spotify':
        if direction == "right" or direction == "left" and count > 30:
          spotifyNavigate(direction)
          direction = ''
          count = 0
          curr_pts.clear()
        elif direction == "up" or direction == "down" and count > 30:
          spotifyVolumeControl(direction)
          direction = ''
          count = 0
          curr_pts.clear()
        elif fingerHold > 10:
          if fingers == 5:
            openSpotify()
          elif fingers == 2:
            spotifyPlayPauseMusic()
          fingerHold = 0
          
      if media == 'netflix':
        if direction == "right" or direction == "left" and count > 30:
          netflixNavigate(direction)
          direction = ''
          count = 0
          curr_pts.clear()
        elif direction == "up" or direction == "down" and count > 30:
          netflixVolumeControl(direction)
          direction = ''
          count = 0
          curr_pts.clear()
        elif fingerHold > 10:
          if fingers == 5:
            openNetflixChrome()
          elif fingers == 2:
            netflixPlayPause()
          fingerHold = 0

      count_2 += 1
    
    # cv2.imshow('mask', mask)
    cv2.putText(frame, direction, (0,100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
    cv2.imshow('Gesture Controlled Media-Player', frame)
    # frame = cv2.drawContours(frame, contours, -1, (0,0,255), 3)
    # try:
    #   cv2.circle(frame, new_pt, 5, (0, 0, 255), -1)
    # except:
    #   pass
    # cv2.imshow('Contours', frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('~'):
      break

  cam.stop()
  cv2.destroyAllWindows()