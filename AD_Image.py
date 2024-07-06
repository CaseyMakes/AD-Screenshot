import win32gui
import win32ui
import win32con
import win32api
from PIL import Image

def capture_window(window_name, region1_coords, region2_coords, save_paths):
    try:
        # Get the window handle of the program
        hwnd = win32gui.FindWindow(None, window_name)
        if not hwnd:
            raise Exception(f"Window '{window_name}' not found!")

        # Get the dimensions of the window
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top

        # Create a device context to capture the screenshot
        hdc = win32gui.GetWindowDC(hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hdc)
        save_dc = mfc_dc.CreateCompatibleDC()

        # Create a bitmap to save the screenshot to
        save_bitmap = win32ui.CreateBitmap()
        save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
        save_dc.SelectObject(save_bitmap)

        # Ensure the window is fully painted before capturing
        win32gui.SetForegroundWindow(hwnd)
        win32gui.UpdateWindow(hwnd)
        win32gui.SendMessage(hwnd, win32con.WM_PAINT, win32con.WM_PAINT, 0)

        # Capture the screenshot and save it to the bitmap
        save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)

        # Convert the bitmap to a PIL Image
        bitmap_bytes = save_bitmap.GetBitmapBits(True)
        image = Image.frombuffer("RGB", (width, height), bitmap_bytes, "raw", "BGRX", 0, 1)

        # Crop the image into two regions and save them
        region1 = image.crop(region1_coords)
        region2 = image.crop(region2_coords)

        region1.save(save_paths[0])
        region2.save(save_paths[1])

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cleanup resources
        try:
            win32gui.DeleteObject(save_bitmap.GetHandle())
            save_dc.DeleteDC()
            mfc_dc.DeleteDC()
            win32gui.ReleaseDC(hwnd, hdc)
        except Exception as cleanup_error:
            print(f"Error during cleanup: {cleanup_error}")

# Set the window name of the program you want to capture
window_name = "Dota 2"

# Coordinates for cropping regions
region1_coords = (262, 140, 580, 950)
region2_coords = (1340, 140, 1652, 950)

# Paths to save the cropped images
save_paths = ["region1.png", "region2.png"]

# Capture the window and save the regions
capture_window(window_name, region1_coords, region2_coords, save_paths)
