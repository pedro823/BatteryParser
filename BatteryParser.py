#!/usr/bin/env python3
from optparse import OptionParser
import subprocess
import sys

text = [
    '# Added by BatteryParser. DO NOT CHANGE THIS LINE.',
    'function battery {',
    '',
    '   echo "$battery"',
    '}',
    '',
    '# end of BatteryParser. DO NOT CHANGE THIS LINE.'
]

color_dict = {
    'black'     : '0;30',   'dark_gray'   : '1;30',
    'red'       : '0;31',   'light_red'   : '1;31',
    'green'     : '0;32',   'light_green' : '1;32',
    'brown'     : '0;33',   'yellow'      : '1;33',
    'blue'      : '0;34',   'light_blue'  : '1;34',
    'purple'    : '0;35',   'light_purple': '1;35',
    'cyan'      : '0;36',   'light_cyan'  : '1;36',
    'light_gray': '0;37',   'white'       : '1;37',
}

error_table = [
    "Tried to open .bashrc, but it is read/write protected.",
    "Some of the tags of the BatteryParser auto-remove have changed. This could have been catastrophic!\n" +
        "You'll have to remove it yourself, in ~/.bashrc. One way to do this would be:" +
        "$ nano ~/.bashrc",

]

def error(e):
    sys.exit("BatteryParser: error: " + error_table[e])

def remove():
    try:
        user = subprocess.check_output(["whoami"]).decode("utf-8").replace("\n", "")
        bashrc = "/home/" + user + "/.bashrc"
        a = open(bashrc, "r")
        write = True
        count = 0
        out = ''
        for line in a.readlines():
            if line == "# Added by BatteryParser. DO NOT CHANGE THIS LINE.":
                write = False
            elif line == "# end of BatteryParser. DO NOT CHANGE THIS LINE.":
                write = True
            if write:
                out += line
            else:
                count += 1
        # Counter limit should be raised if new features are added.
        if count > 8:
            error(1)
        a.close()
        a = open(bashrc, "w")
        a.write(out)
    except IOError:
        error(0)

def batteryScan():
    subprocess.call("clear")
    print("=== BATTERY SCAN ===")
    power = subprocess.check_output(["upower", "-e"]).decode('utf-8').strip().split("\n")
    for line in power:
        print(line)
    print("Which one seems to be the battery?")
    print("(Note: it should look something like /org/freedesktop/UPower/devices/battery_BAT1)")
    correctpower = input(" > /org/freedesktop/UPower/devices/")
    compound = "/org/freedesktop/UPower/devices/" + correctpower
    while compound not in power:
        print("Uh-oh! That is not a valid option.")
        for line in power:
            print(line)
        print("Which one seems to be the battery?")
        print("(Note: it should look something like /org/freedesktop/UPower/devices/battery_BAT1)")
        correctpower = input(" > /org/freedesktop/UPower/devices/")
        compound = "/org/freedesktop/UPower/devices/" + correctpower
    return compound

def chooseColor():
    no_color = "\033[0m"
    subprocess.call("clear")
    print("=== CHOOSE COLOR ===")
    print("Available colors: \n\n")
    for name, color in color_dict.items():
        print("\033[" + color + name + no_color)
    print("Which color do you want the battery plugin to appear as?")
    confirm = input(" > ")
    while confirm not in color_dict:
        print("Not a valid color.")
        confirm = input(" > ")
    return confirm

def main():
    ps = OptionParser()
    parser.addOption("-n", "--notreally",
        action = "store_true",
        dest = "actual",
        default = False,
        help = "Doesn't actually export PS1 to .bashrc. Instead, show what it would do."
    )
    parser.addOption("-r", "--remove",
        action = "store_true",
        dest = "remove",
        help = "Removes battery plugin from .bashrc."
    )
    (flags, args) = ps.parse_args()
    if flags.remove:
        print("Sad to see you go :(")
        print("Removing battery from .bashrc...")
        remove()
        print("Done! sourcing new .bashrc...")
        subprocess.Popen(". ~/.bashrc", shell = True)
        exit(0)
    else:
        print("=== BatteryParser INSTALLER ===")
        print("SCANNING BATTERY:")
        battery = batteryScan()
        for line in subprocess.check_output(["upower", "-i", battery]).strip.split('\n')
            print(line)
        print("Does this seem correct? (y/n)")
        correct = input(" > ")
        while correct != "y" and correct != "n":
            print("Does this seem correct? (y/n)")
            correct = input(" > ")
        if correct == "n":
            print("Battery is not correct: Exiting program. Please run it again.")
            exit(0)
        color = chooseColor()
        subprocess.Popen([""])

if (__name__ == "__main__"):
    main()
