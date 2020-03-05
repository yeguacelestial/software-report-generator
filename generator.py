import wmi
import winreg

class ReportGenerator():

    def __init__(self):
        self.conexion = wmi.WMI()

    def programas_win10_store(self):
        resultados = {}

        try:
            for info in self.conexion.Win32_InstalledStoreProgram():
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
                if app_name in resultados:
                    continue
                if app_name not in resultados:
                    resultados[app_name] = []

                resultados[app_name] = [vender, info.Version, 'Desconocida']
        except:
            pass

        for k, v in resultados.items():
            print(f'Aplicación: {k} - Fabricante: {v[0]} - Version: {v[1]} - Fecha de instalación: {v[2]}')

    def programas_productos(self):
        resultados = {}

        try:
            for info in self.conexion.Win32_Product():
                app_name = str(info.Name).encode('utf8','ignore').decode()
                vendor = str(info.Vendor).encode('utf8', 'ignore').decode()

                if app_name not in resultados:
                    resultados[app_name] = []
                resultados[



                app_name] = [vendor, info.Version, info.InstallDate]

        except:
            pass

        for k, v in resultados.items():
            print(f'Aplicación: {k} - Fabricante: {v[0]} - Version: {v[1]} - Fecha de instalación: {v[2]}')

    def programas_win10(self):
        resultados = {}

        try:
            for info in self.conexion.Win32_InstalledWin32Program():
                app_name = str(info.Name).encode('utf8', 'ignore').decode()
                vendor = str(info.Vendor).encode('utf8', 'ignore').decode()

                if app_name not in resultados:
                    resultados[app_name] = []
                resultados[app_name] = [vendor, info.Version, 'Desconocida']

        except:
            pass

        for k, v in resultados.items():
            print(f'Aplicación: {k} - Fabricante: {v[0]} - Version: {v[1]} - Fecha de instalación: {v[2]}')

generador = ReportGenerator()

generador.programas_win10_store()
generador.programas_productos()
generador.programas_win10()
