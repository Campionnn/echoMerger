from pynput import mouse
from pynput.keyboard import Key, Listener
import win32gui


window_name = "Wuthering Waves  "


def main():
    window_rect = win32gui.GetWindowRect(win32gui.FindWindow(None, window_name))
    # print width and height
    width = window_rect[2] - window_rect[0]
    height = window_rect[3] - window_rect[1]
    print(width, height)

    mouse_controller = mouse.Controller()

    # click in middle of window
    # mouse_controller.position = (window_rect[0] + width // 2, window_rect[1] + height // 2)
    # mouse_controller.click(mouse.Button.left, 1)

    # click bottom right of window
    mouse_controller.position = (window_rect[2], window_rect[3])
    mouse_controller.click(mouse.Button.left, 1)

# def callback(hwnd, extra):
#     rect = win32gui.GetWindowRect(hwnd)
#     x = rect[0]
#     y = rect[1]
#     w = rect[2] - x
#     h = rect[3] - y
#     print("Window %s:" % win32gui.GetWindowText(hwnd))
#     print("\tLocation: (%d, %d)" % (x, y))
#     print("\t    Size: (%d, %d)" % (w, h))
#
# def main():
#     win32gui.EnumWindows(callback, None)


if __name__ == "__main__":
    main()
