import ctypes


def get_working_area():
    # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-systemparametersinfoa
    SPI_GETWORKAREA = 0x0030

    # An array of four LONG values (left, top, right, bottom)
    rect = (ctypes.c_long * 4)()  # ignore pycharm type-hint warning

    # Call SystemParametersInfoA to get the work area
    ctypes.windll.user32.SystemParametersInfoA(SPI_GETWORKAREA, 0, rect, 0)

    width = rect[2] - rect[0]  # right - left
    height = rect[3] - rect[1]  # bottom - top

    return width, height


def set_app_window(hwnd):
    # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowlongw
    # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowlongw
    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080

    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    style = style & ~WS_EX_TOOLWINDOW
    style = style | WS_EX_APPWINDOW
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
