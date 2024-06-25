import threading
import keyboard
import os
from merger import Merger
from scanner import Scanner
from reader import Reader


def kill():
    keyboard.wait('esc')
    print("esc key detected... quitting")
    os._exit(0)


def main():
    merger = Merger()
    scanner = Scanner(merger.window_handle, merger.window_rect)
    reader = Reader(merger.window_handle, merger.window_rect)

    threading.Thread(target=kill).start()

    # print(scanner.find_echos_order(scanner.screenshot("buh")))

    merger.set_window_foreground()
    merger.wake_up()
    while True:
        merger.merge()
        order = scanner.find_echos_order(scanner.screenshot())
        merger.wake_up()
        print(order)
        if len(order) == 0:
            raise ValueError(f"Invalid order: {order}")
        for i in order:
            if i == "gold":
                merger.select()
                im = reader.screenshot()
                merger.wake_up()
                echo_cost = reader.find_cost(im)
                echo_main = reader.find_main(im, echo_cost)
                echo_set = reader.find_set(im)
                print(f"Found: {echo_set} : {echo_main} : {echo_cost}")
                if echo_cost not in [1, 3]:
                    raise ValueError(f"Invalid cost: {echo_cost}")
                if echo_main is None:
                    raise ValueError(f"Invalid main: {echo_main}")
                if echo_set is None:
                    raise ValueError(f"Invalid set: {echo_set}")
                if lock_echo(echo_cost, echo_main, echo_set):
                    print(f"Locked: {echo_set} : {echo_main} : {echo_cost}")
                    merger.lock()
                merger.back()
                merger.next()
            else:
                merger.next()
        merger.back()


def lock_echo(echo_cost, echo_main, echo_set):
    if echo_cost == 1 and echo_main == "ATK":
        return True
    if echo_cost == 1 and echo_set == "Rejuvenating Glow" and echo_main == "HP":
        return True
    if echo_main == "Energy Regen":
        return True
    if echo_cost == 3 and echo_set in ["Moonlit Clouds", "Lingering Tunes"] and (echo_main not in ["HP", "ATK", "DEF"]):
        return True
    if echo_set == "Freezing Frost" and echo_main == "Glacio DMG Bonus":
        return True
    if echo_set == "Molten Rift" and echo_main == "Fusion DMG Bonus":
        return True
    if echo_set == "Void Thunder" and echo_main == "Electro DMG Bonus":
        return True
    if echo_set == "Sierra Gale" and echo_main == "Aero DMG Bonus":
        return True
    if echo_set == "Celestial Light" and echo_main == "Spectro DMG Bonus":
        return True
    if echo_set == "Sun-sinking Eclipses" and echo_main == "Havoc DMG Bonus":
        return True
    return False


if __name__ == "__main__":
    main()
