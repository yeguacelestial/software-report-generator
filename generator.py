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

    def reporte(self, direccion, nombre="reporte"):

        try:
            if direccion[-1] != '\\':
                direccion = direccion + "\\"

            if nombre == None:
                nombre = "reporte"

            else:
                nombre = f'\\{nombre}'

            direccion_final = direccion + nombre + ".pdf"
            pdf = canvas.Canvas(direccion_final)
            print(f"[+] Generando reporte como {nombre}.pdf...")

            table_data = [["APP", "FABRICANTE", "VERSION", "FECHA DE INSTALACION"]]

            def escribir(diccionario):
                i = 0

                for k, v in diccionario:
                    table_data.append([k,v[0],v[1],v[2]])
                    pdf.setFont('Helvetica', 8)
                    pdf.drawString(50, 800-i, str(f'Aplicacion: {k} - Fabricante: {v[0]} - Version: {v[1]} - Fecha de instalacion: {v[2]}'))
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

            # PC Details
            # Serial Number of Motherboard and OS
            import os, sys
            def numero_serial():
                os_type = sys.platform.lower()

                if "win" in os_type:
                    command = "wmic bios get serialnumber"

                elif "linux" in os_type:
                    command = "hal-get-property --udi /org/freedesktop/Hal/devices/computer --key system.hardware.uuid"

                return os.popen(command).read().replace("\n","").replace("	","").replace(" ","")
            serial = numero_serial()
            serial = f"NUMERO SERIAL DEL PC: {serial}"

            import platform
            sistema_operativo = platform.platform()
            sistema_operativo = f"SISTEMA OPERATIVO: {sistema_operativo}"

            # Create Pararaph objects
            from reportlab.platypus import Paragraph
            from reportlab.lib.styles import getSampleStyleSheet
            styles = getSampleStyleSheet()
            styleN = styles['Normal']

            P_serial = Paragraph(serial, styleN)
            P_os = Paragraph(sistema_operativo, styleN)
            firma = Paragraph("Firma:____________________________________________\n", styleN)

            elems = []
            elems.append(firma)
            elems.append(P_serial)
            elems.append(P_os)

        # START TABLE
            from reportlab.platypus import SimpleDocTemplate
            from reportlab.lib.pagesizes import letter, A4, landscape

            pdf_table = SimpleDocTemplate(
                f"{nombre}.pdf",
                pagesize = A4
            )
            pdf_table.pagesize = landscape(A4)

            from reportlab.platypus import Table

            from reportlab.lib.units import inch
            colwidths = [2.8*inch] * len(table_data)
            rowheights = [.5*inch] * len(table_data)

            table = Table(table_data, colwidths, rowheights)

            # Add style
            from reportlab.platypus import TableStyle, Paragraph
            from reportlab.lib import colors
            style = TableStyle([
                    ('BACKGROUND', (0,0), (3,0), colors.green),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),

                    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),

                    ('FONTAME', (0,0), (-1,0), 'Courier-Bold'),
                    ('FONTSIZE', (0,0), (-1,-1), 10),
                    ('FONTSIZE', (0,1), (0,-1), 8),

                    ('BOTTOMPADDING', (0,0), (-1,0), 12),

                    ('BACKGROUND', (0,1), (-1,-1), colors.beige),

                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ])
            table.setStyle(style)

            print("[+] Tabla generada.")
        # END TABLE

            elems.append(table)
            pdf_table.build(elems)

            pdf.save()
            print(f"[+] Reporte {nombre}.pdf generado en {direccion_final}")

        except IOError as e:
            print(e)
            print("[-] El directorio no existe, o no hay suficientes permisos para generar el reporte.")
            print("[*] TIP: Si el directorio existe, escribelo entre comillas.")

        except Exception as e:
            print(e)
            print(f"[*] Usa el comando -h o --help para consultar los comandos de uso del programa.")
            exit