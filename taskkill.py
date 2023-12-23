import subprocess
import time
import platform
def kill_vlc_process():
    # Determine the platform (Windows or Unix-like)
    current_platform = platform.system()

    if current_platform == "Windows":
        # Kill VLC process on Windows using taskkill
        subprocess.run(["taskkill", "/F", "/IM", "vlc.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(1)
        subprocess.run(["taskkill", "/F", "/IM", "vlc"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f'Proceso VLC.EXE Terminado'*3)
    elif current_platform in ["Linux", "Darwin"]:
        # Kill VLC process on Unix-like systems using pkill
        subprocess.run(["pkill", "vlc"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        print("Unsupported operating system")
