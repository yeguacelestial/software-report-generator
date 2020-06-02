import os, sys

def getMachine_addr():
    os_type = sys.platform.lower()

    if "win" in os_type:
        command = "wmic bios get serialnumber"

    elif "linux" in os_type:
        command = "hal-get-property --udi /org/freedesktop/Hal/devices/computer --key system.hardware.uuid"

    return os.popen(command).read().replace("\n","").replace("	","").replace(" ","")

print(getMachine_addr())