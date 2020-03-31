import wmi
import winreg

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import PageBreak
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.tables import Table

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

        resultados = resultados.items()

        return resultados

    def programas_productos(self):
        resultados = {}

        try:
            for info in self.conexion.Win32_Product():
                app_name = str(info.Name).encode('utf8','ignore').decode()
                vendor = str(info.Vendor).encode('utf8', 'ignore').decode()

                if app_name not in resultados:
                    resultados[app_name] = []
                resultados[app_name] = [vendor, info.Version, info.InstallDate]

        except:
            pass

        resultados = resultados.items()

        return resultados

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

        resultados = resultados.items()

        return resultados

    def reporte(self, direccion, nombre):

        try:
            nombre = f'\\{nombre}'
            direccion_final = direccion + nombre + ".pdf"
            pdf = canvas.Canvas(direccion_final)

            print("[+] Generando reporte...")
            
            def escribir(diccionario):
                i = 0

                for k, v in diccionario:
                    pdf.setFont('Helvetica', 8)
                    pdf.drawString(50, 800-i, str(f'Aplicación: {k} - Fabricante: {v[0]} - Version: {v[1]} - Fecha de instalación: {v[2]}'))
                    i += 20

                    if 800-i < 50:
                        pdf.showPage()
                        i = 0
                pdf.showPage()


            apps_store = self.programas_win10_store()
            apps_productos = self.programas_productos()
            apps_win10 = self.programas_win10()

            escribir(apps_store)
            escribir(apps_productos)
            escribir(apps_win10)

            pdf.save()

            print(f"[+] Reporte generado en {direccion_final}")

        except Exception as e:
            print(f"[-] Error: {e}")
            exit


#generador = ReportGenerator()
#generador.reporte('D:\\prueba')

# TODO:
# - Espacio para la firma
# - Inputs del usuario (direccion, nombre del archivo)
