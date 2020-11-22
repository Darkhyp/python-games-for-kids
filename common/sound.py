## system sounds
from sys import platform
if platform == "win32":
    import winsound
elif platform == 'linux' or platform=='darwin':
    import os

def make_sound(sound_map):
    if sound_map==1:
        if platform == "win32":
            winsound.PlaySound('SystemAsterisk', winsound.SND_ASYNC)
        elif platform == 'linux':
            os.system('aplay bounce.wav')
        elif platform == 'darwin':
            os.system('afplay bounce.wav')
    if sound_map == 2:
        if platform == "win32":
            winsound.MessageBeep()
    elif sound_map == 3:
        if platform == "win32":
            winsound.PlaySound("SystemHand", winsound.SND_ASYNC)
    elif sound_map == 4:
        if platform == "win32":
            winsound.PlaySound('SystemExit', winsound.SND_ASYNC)
    elif sound_map == 5:
        pass

