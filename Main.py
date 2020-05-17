from MotionTrack import *

media = input('Enter media software you are using (spotify/netflix): ')

print('Please enter the HSV range of the hand being detected if the format "(x,y,z)"\nFor default settings, click enter (The default will be blue)')
lower = input('Enter the lower HSV for the range being detected: ')
higher = input('Enter the higher HSV for the range being detected: ')

try:
  lower = lower[1:-2].split(',')
  lower = (int(lower[0]), int(lower[1]), int(lower[2]))
  higher = higher[1:-2].split(',')
  higher = (int(higher[0]), int(higher[1]), int(higher[2]))
  motionTrack(media, (lower, higher))
except:
  print('Using default color range')
  motionTrack(media)