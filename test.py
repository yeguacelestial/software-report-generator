import wmi

# Connection to local machine
c = wmi.WMI()

# List all running processes
for process in c.Win32_Process():
    print(process.ProcessId, process.Name)
