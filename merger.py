import time
import win32gui
import vgamepad as vg

window_name = "Wuthering Waves  "  # idk why kuro added spaces to the end of the window name
press_delay = 0.05
key_delay = 0.5
open_delay = 0.5


class Merger:
    def __init__(self):
        self.window_handle = win32gui.FindWindow(None, window_name)
        self.window_rect = win32gui.GetWindowRect(self.window_handle)

        self.gamepad = vg.VX360Gamepad()

    def set_window_foreground(self):
        win32gui.SetForegroundWindow(self.window_handle)

    def wake_up(self):
        self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
        self.gamepad.update()
        time.sleep(1)
        self.gamepad.reset()
        self.gamepad.update()

    def merge(self):
        self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
        self.gamepad.update()
        time.sleep(press_delay)
        self.gamepad.reset()
        self.gamepad.update()
        time.sleep(key_delay)
        self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
        self.gamepad.update()
        time.sleep(press_delay)
        self.gamepad.reset()
        self.gamepad.update()
        time.sleep(4)

    def select(self):
        self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        self.gamepad.update()
        time.sleep(press_delay)
        self.gamepad.reset()
        self.gamepad.update()
        time.sleep(open_delay)

    def lock(self):
        self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
        self.gamepad.update()
        time.sleep(press_delay)
        self.gamepad.reset()
        self.gamepad.update()
        time.sleep(key_delay)

    def back(self):
        self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        self.gamepad.update()
        time.sleep(press_delay)
        self.gamepad.reset()
        self.gamepad.update()
        time.sleep(key_delay)

    def next(self):
        self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
        self.gamepad.update()
        time.sleep(press_delay)
        self.gamepad.reset()
        self.gamepad.update()
        time.sleep(key_delay)
