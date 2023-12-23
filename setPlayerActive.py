import pygetwindow as gw
import time

# Wait for VLC to open
def videoActiveWindow():

    #time.sleep(5)

    # Get a list of all open windows

    try:
        windows = gw.getAllWindows()

        # Iterate through the windows and find the one with "vlc.exe" in the title
        vlc_window = None
        for window in windows:
            # print(window)
            if "vlc" in window.title.lower():
                vlc_window = window
                break
        for window in windows:
            if "mainpichon" in window.title.lower():
                mainpichon_window = window
                break
        # Bring the VLC window to the foreground
        if vlc_window:
            vlc_window.activate()
            print(f"{vlc_window.title} is now the active window.")
        else:
            print("VLC window not found.")
        if mainpichon_window:
            mainpichon_window.minimize()
            print(f"{mainpichon_window.title} is now the active window.")
        else:
            print("VLC window not found.")


    except:
        pass
    finally:
        return None
videoActiveWindow()