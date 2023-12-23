import setPlayerActive
import random
import psutil
import cv2
import pygetwindow as gw
import pyautogui
import numpy as np
import time
import subprocess
import platform

# Set the path to your VLC executable
VLC_PATH = "C:/Program Files/VideoLAN/VLC/vlc.exe"

# Set the video stream URL
VIDEO_URL = []
VIDEO_URL.append("http://smartersplayer.live:8080/play/MWJq4mvXkXHV8hydmt6MVXB5x--g9v_Nw8WQL8s4riM/ts") #VOLVER
VIDEO_URL.append("http://smartersplayer.live:8080/play/MWJq4mvXkXHV8hydmt6MVXB5x--g9v_Nw8WQL8s4riM/ts") #VOLVER
#VIDEO_URL.append("http://smartersplayer.live:8080/play/MWJq4mvXkXHV8hydmt6MVZ3AbWwKCrMgqHUqnuCdiDmp67s_b03PScXxHUDfhj4V/ts")   #(HQ RECTV)
#VIDEO_URL.append("http://smartersplayer.live:8080/play/MWJq4mvXkXHV8hydmt6MVcslcRGe8fvrKy4kFWKQkQKkppiqRrE2Kt6nK3aRhi0G/ts")   #(FHD RECTV)
VIDEO_URL_RAND = random.choice(VIDEO_URL)
# Set the time interval for frame comparison (in seconds)
FRAME_INTERVAL = 5

def get_process_id_by_name(process_name):
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == process_name:
            return process.info['pid']
    return None

# Function to terminate a process by ID
def terminate_process_by_id(process_id):
    try:
        process = psutil.Process(process_id)
        process.terminate()
        print(f"Process with ID {process_id} terminated successfully.")
    except psutil.NoSuchProcess as e:
        print(f"Error: {e}")



def capture_frame(window_title):
    try:
        # Get the window by title
        window = gw.getWindowsWithTitle(window_title)[0]

        # Get window position and size
        x, y, width, height = window.left, window.top, window.width, window.height

        # Capture the screen within the window region
        screenshot = pyautogui.screenshot(region=(x, y, width, height))

        # Convert the screenshot to a NumPy array and then to a BGR image
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        return frame
    except IndexError:
        print(f"Error: Window with title '{window_title}' not found.")
        return None
    finally:
        pass


def are_frames_equal(frame1, frame2):
    try:
        # Convert frames to grayscale for comparison
        gray_frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray_frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        # Compute the absolute difference between frames
        difference = cv2.absdiff(gray_frame1, gray_frame2)
        _, threshold = cv2.threshold(difference, 30, 255, cv2.THRESH_BINARY)
        # Count non-zero pixels
        non_zero_pixels = cv2.countNonZero(threshold)

    except:
        print(f'Error in frame size')
        non_zero_pixels = 300000
    finally:
        pass

    # Threshold the difference image
    print(f'non_zero_pixels == {non_zero_pixels}' )

    return non_zero_pixels == 0


def is_video_frozen(window):
    try:
        start_time = time.time()
        frame1 = capture_frame(window)

        while time.time() - start_time < FRAME_INTERVAL:
            time.sleep(1)
            frame2 = capture_frame(window)

            if frame1 is not None and frame2 is not None:
                # Compare consecutive frames
                difference = cv2.absdiff(frame1, frame2)
                _, threshold = cv2.threshold(difference, 30, 255, cv2.THRESH_BINARY)
                non_zero_pixels = cv2.countNonZero(cv2.cvtColor(threshold, cv2.COLOR_BGR2GRAY))

                if non_zero_pixels > 0:
                #if cv2.countNonZero(threshold) > 0:
                    # Frames are different, video is not frozen
                    return False
            else:
                if frame1 == None or frame2 == None:
                    process_name = "vlc.exe"  # Replace with the actual process name
                    vlc_process_id = get_process_id_by_name(process_name)
                    if vlc_process_id is not None:
                        print(f"Process ID of {process_name}: {vlc_process_id}")
                        terminate_process_by_id(vlc_process_id)
                    else:
                        pass
                    time.sleep(2)
                    restart_vlc()

        # Video appears to be frozen
        return True
    except:
        print(f'Error la comparar FRAMES')
        return False

def restart_vlc():
    process=subprocess.Popen([VLC_PATH,"--fullscreen","--volume", "150", VIDEO_URL_RAND])
    #process.wait()  # Wait for the process to finish
    return_code = process.returncode
    print(f'Process has returned code = {return_code}')

def main():
    # Set the title of the video player window
    #windowTittleCurrent= windowTittle.get_window_title("vlc.exe")
    video_player_title = []
    #video_player_title.append(windowTittleCurrent)
    video_player_title.append("ts - Reproductor multimedia VLC")

    try:
        while True:
            # Capture the first frame
            setPlayerActive.videoActiveWindow()
            frame1 = capture_frame(video_player_title[0])

            if frame1 is not None:
                # Wait for the specified interval
                time.sleep(FRAME_INTERVAL)

                # Capture the second frame
                frame2 = capture_frame(video_player_title[0])

                if frame2 is not None:
                    # Compare frames
                    if are_frames_equal(frame1, frame2):
                        print("Video is frozen")
                        process_name = "vlc.exe"  # Replace with the actual process name
                        vlc_process_id = get_process_id_by_name(process_name)
                        if vlc_process_id is not None:
                            print(f"Process ID of {process_name}: {vlc_process_id}")
                            terminate_process_by_id(vlc_process_id)
                        else:
                            pass
                        time.sleep(2)
                        restart_vlc()
                        time.sleep(10)

                    else:
                        print("Video is live")
            else:
                if frame1 is None:
                    process_name = "vlc.exe"  # Replace with the actual process name
                    vlc_process_id = get_process_id_by_name(process_name)
                    if vlc_process_id is not None:
                        print(f"Process ID of {process_name}: {vlc_process_id}")
                        terminate_process_by_id(vlc_process_id)
                    else:
                        pass
                    time.sleep(2)
                    restart_vlc()
                    time.sleep(10)
    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C)
        pass


if __name__ == "__main__":
    main()
