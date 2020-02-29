import wmi

# Connection to local machine
c = wmi.WMI()

# List all running processes
for process in c.Win32_Process():
    print(process.ProcessId, process.Name)

# Percentage of free space for each fixed disk in the system
for disk in c.Win32_LogicalDisk(DriveType=3):
    print(disk.Caption, "%0.2f%% free" % (100.0*float(disk.FreeSpace) / float(disk.Size)))
