from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from pynput.keyboard import Key, Controller as KeyController
from ctypes import wintypes
import ctypes
import pycaw

def set_volume(percent):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(percent / 100.0, None)

def change_volume(delta):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
    current = volume.GetMasterVolumeLevelScalar()
    volume.SetMasterVolumeLevelScalar(min(max(0.0, current + delta), 1.0), None)

keyboard = KeyController()

def media_play_pause():
    keyboard.press(Key.media_play_pause)
    keyboard.release(Key.media_play_pause)

def media_next():
    keyboard.press(Key.media_next)
    keyboard.release(Key.media_next)

def media_previous():
    keyboard.press(Key.media_previous)
    keyboard.release(Key.media_previous)

def media_stop():
    keyboard.press(Key.media_stop)
    keyboard.release(Key.media_stop)