from generator import ReportGenerator
import pkg_resources.py2_warn

def main():
    print("**** GENERADOR DE REPORTES DE SOFTWARE INSTALADOS ****")
    print("[!] Para un reporte mas completo, ejecuta el programa como administrador.")
    
    get_input = input_options()

    nombre = get_input[0]
    if len(nombre) == 0: nombre = None

    generador = ReportGenerator()
    generador.reporte('\\', nombre)

    firmar = get_input[1]

    if firmar == "si" or firmar == "Si" or firmar == "SI":
        if nombre is not None:
            firmar_mifiel(reporte=f'{nombre}.pdf')
        else:
            firmar_mifiel(reporte='reporte.pdf')

        print("[+] Se enviaron las firmas a la plataforma MIFIEL de todos los destinatarios.")

    else:
        pass
    
    finalizar = input("[+] El programa finalizo. Presiona Enter para salir...")

def input_options():
    options = []
    nombre = input("[*] Nombre del archivo (Default: reporte.pdf) => ")
    firmar = input("[*] ¿Desea mandar a firmar electronicamente el archivo (MIFIEL Sandbox)? si|[no] => ")
    options.append(nombre)
    options.append(firmar)
    return options


def firmar_mifiel(reporte='reporte.pdf'):
    from mifiel import Document, Client

    app_id = input("[*] Introduce el token APP ID (Mifiel API): ")
    if len(app_id) == 0: 
        print("[-] Por favor, introduce un token correcto. ") 
        firmar_mifiel(reporte)

    app_secret = input("[*] Introduce el token APP SECRET (Mifiel API): ")
    if len(app_secret) == 0:
        print("[-] Por favor, introduce un token correcto. ")
        firmar_mifiel(reporte)

    client = Client(app_id=app_id, secret_key=app_secret)
    client.use_sandbox()

    print("[!] Las personas que van a firmar deben estar registradas en https://app-sandbox.mifiel.com.")
    cantidad_firmas = input("[*] ¿Cuántas personas van a firmar?: ")
    if len(cantidad_firmas) == 0: return print("[-] Error: cantidad de firmas no valida.")

    try:
        cantidad_firmas = int(cantidad_firmas)

        firmas =[]
        for persona in range(0, cantidad_firmas):
            firma = {}

            nombre = input(f"[*] Nombre completo de la persona {persona+1}: ")
            email = input(f"[*] Correo electronico de la persona {persona+1}: ")
            rfc_curp = input(f"[*] CURP o RFC de la persona {persona+1}: ")

            firma['name'] = nombre
            firma['email'] = email
            firma['rfc_curp'] = rfc_curp
            firmas.append(firma)

        document = Document.create(
            client = client,
            signatories = firmas,
            file=f'{reporte}'
        )

    except:
        raise
        print("[-] Cantidad de firmas invalida.")
        exit()


if __name__ == '__main__':
    main()