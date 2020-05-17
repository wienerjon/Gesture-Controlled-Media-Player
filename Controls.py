import time
import pyautogui

def waitTimeAfter():
  time.sleep(0.01)

#spotify
def openSpotify():
  pyautogui.hotkey('command', 'space')
  # time.sleep(2)
  pyautogui.typewrite('Spotify')
  # time.sleep(1)
  pyautogui.hotkey('enter')
  time.sleep(4)

def spotifyPlayPauseMusic():
  pyautogui.hotkey('space')
  waitTimeAfter()
      
def spotifyVolumeControl(direction, isMax=False):
  if isMax:
    pyautogui.hotkey('command', 'shift', direction)
  else:
    pyautogui.hotkey('command', direction)

def spotifyNavigate(direction):
  pyautogui.hotkey('command', 'ctrl', direction)

#netflix 
def openNetflixChrome():
  pyautogui.keyDown('command')
  pyautogui.press('space')
  pyautogui.keyUp('command')
  time.sleep(2)
  pyautogui.typewrite('chrome')
  time.sleep(1)
  pyautogui.hotkey('enter')
  time.sleep(4)

def netflixPlayPause():
  pyautogui.hotkey('space')
  waitTimeAfter()

def netflixVolumeControl(direction):
  pyautogui.hotkey(direction)

def netflixNavigate(direction):
  pyautogui.hotkey(direction)

