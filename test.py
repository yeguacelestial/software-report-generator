import wmi
import winreg

# Connection to local machine
c = wmi.WMI()

# # List all running processes
# for process in c.Win32_Process():
#     print(process.ProcessId, process.Name)
#
# # Percentage of free space for each fixed disk in the system
# for disk in c.Win32_LogicalDisk(DriveType=3):
#     print(disk.Caption, "%0.2f%% free" % (100.0*float(disk.FreeSpace) / float(disk.Size)))
#
# # Show IP and MAC addresses for IP-enabled network interfaces
# for interface in c.Win32_NetworkAdapterConfiguration (IPEnabled=1):
#     print (interface.Description, interface.MACAddress)
#     for ip_address in interface.IPAddress:
#         print (ip_address)
#
# # Display what's running on startup
# for s in c.Win32_StartupCommand():
#     print(f"[{s.Location}] {s.Caption} <{s.Command}>")

# # List registry keys on system
# r = wmi.Registry()
# result, names = r.GetStringValue(
#     hDefKey = winreg.HKEY_LOCAL_MACHINE,
#     sSubKeyName="Software"
# )
# for key in names:
#     print(key)

def get_all_installed_win10_store():
    results = {}

    try:
        for info in c.Win32_InstalledStoreProgram():
            if '-' in info.Name:
                continue
            app_name = str(info.Name).encode('utf8', 'ignore').decode()

            if not info.Vendor:
                vender = 'None'
            if '-' in info.Vendor:
                vender = 'None'
            else:
                vendor = str(info.Vendor).encode('utf8', 'ignore').decode()
                vender = vendor.split(', ')[0].split('=')[-1].strip()
            if app_name in results:
                continue
            if app_name not in results:
                results[app_name] = []

            results[app_name] = [vender, info.Version, 'Desconocida']
    except:
        pass

    for k, v in results.items():
        print(f'Aplicación: {k} - Fabricante: {v[0]} - Version: {v[1]} - Fecha de instalación: {v[2]}')

    #return results

def get_installed_product_software():
    results = {}

    try:
        for info in c.Win32_Product():
            app_name = str(info.Name).encode('utf8','ignore').decode()
            vendor = str(info.Vendor).encode('utf8', 'ignore').decode()

            if app_name not in results:
                results[app_name] = []
            results[app_name] = [vendor, info.Version, info.InstallDate]

    except:
        pass
    
    for k, v in results.items():
        print(f'Aplicación: {k} - Fabricante: {v[0]} - Version: {v[1]} - Fecha de instalación: {v[2]}')
    
    #return results

def get_all_installed_win10_software():
    results = {}

    try:
        for info in c.Win32_InstalledWin32Program():
            app_name = str(info.Name).encode('utf8', 'ignore').decode()
            vendor = str(info.Vendor).encode('utf8', 'ignore').decode()

            if app_name not in results:
                results[app_name] = []
            results[app_name] = [vendor, info.Version, 'Desconocida']

    except:
        pass

    for k, v in results.items():
        print(f'Aplicación: {k} - Fabricante: {v[0]} - Version: {v[1]} - Fecha de instalación: {v[2]}')

    #return results