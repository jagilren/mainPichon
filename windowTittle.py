import psutil
import ctypes

def get_window_title(process_name):
    # Get the process ID by name
    process_id = None
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == process_name:
            process_id = process.info['pid']
            break

    if process_id is not None:
        # Get the window title
        hwnd = ctypes.windll.user32.FindWindowW(None, None)  # Get the first window handle
        while hwnd:
            current_pid = ctypes.c_ulong()
            ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(current_pid))
            if current_pid.value == process_id:
                length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
                buffer = ctypes.create_unicode_buffer(length + 1)
                ctypes.windll.user32.GetWindowTextW(hwnd, buffer, length + 1)
                return buffer.value
            hwnd = ctypes.windll.user32.GetWindow(hwnd, 2)  # Get the next window handle

    return None

# Example usage for VLC
process_name = "vlc.exe"
window_title = get_window_title(process_name)

if window_title is not None:
    print(f"Window title of {process_name}: {window_title}")
else:
    print(f"{process_name} is not running or has no visible window.")
