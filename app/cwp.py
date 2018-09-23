import os
import random


# Change Wallpaper via Terminal Command
def changeWallpaper():
    # Go to downloads
    os.chdir('downloads')
    # Create full path of every file in directory
    files = [os.path.abspath(x) for x in os.listdir()]
    # Choose a random path from the list of 'em
    wallpaper = random.choice(files)
    # Execute wallpaper change command with random file name
    command = "gsettings set org.gnome.desktop.background picture-uri 'file://%s'" % wallpaper
    os.system(command)
    # Confirm it
    print('Changed wallpaper to ' + wallpaper)
    return


changeWallpaper()
