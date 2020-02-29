import wmi

# Connection to local machine
c = wmi.WMI()

# List all running processes
for process in c.Win32_Process():
    print(process.ProcessId, process.Name)

# Percentage of free space for each fixed disk in the system
for disk in c.Win32_LogicalDisk(DriveType=3):
    print(disk.Caption, "%0.2f%% free" % (100.0*float(disk.FreeSpace) / float(disk.Size)))

# Show IP and MAC addresses for IP-enabled network interfaces
for interface in c.Win32_NetworkAdapterConfiguration (IPEnabled=1):
    print (interface.Description, interface.MACAddress)
    for ip_address in interface.IPAddress:
        print (ip_address)

# Display what's running on startup
for s in c.Win32_StartupCommand():
    print(f"[{s.Location}] {s.Caption} <{s.Command}>")
