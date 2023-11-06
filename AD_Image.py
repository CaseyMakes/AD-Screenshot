import win32gui
import win32ui
import win32con
import win32api
from PIL import Image

# Set the window name of the program you want to capture
window_name = "Dota 2"

# Get the window handle of the program
hwnd = win32gui.FindWindow(None, window_name)

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

# Capture the screenshot and save it to the bitmap
win32gui.SetForegroundWindow(hwnd)
win32gui.SendMessage(hwnd, win32con.WM_PAINT, win32con.WM_PAINT, 0)
save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)

# Convert the bitmap to a PIL Image
bitmap_bytes = save_bitmap.GetBitmapBits(True)
image = Image.frombuffer("RGBA", (width, height), bitmap_bytes, "raw", "RGBA", 0, 1)

# Crop the image into two regions
region1 = image.crop((262, 140, 580, 950))
region2 = image.crop((1340, 140, 1652, 950))

# Save the two regions as separate PNG files
region1.save("region1.png")
region2.save("region2.png")

# Cleanup
win32gui.DeleteObject(save_bitmap.GetHandle())
save_dc.DeleteDC()
mfc_dc.DeleteDC()
win32gui.ReleaseDC(hwnd, hdc)
