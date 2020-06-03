from generator import ReportGenerator
from optparse import OptionParser

def main():
    get_input = input_options()

    options = get_input[0]
    arguments = get_input[1]

    nombre = options.nombre

    generador = ReportGenerator()
    generador.reporte('\\', nombre)

    firmar = options.firmar

    if firmar == "si" or firmar == "Si" or firmar == "SI":
        if nombre is not None:
            firmar_mifiel(reporte=f'{nombre}.pdf')
        else:
            firmar_mifiel(reporte='reporte.pdf')

        print("[+] Se enviaron las firmas a la plataforma MIFIEL de todos los destinatarios.")

    else:
        pass


def input_options():
    parser = OptionParser(usage="\n\nUso: gestor.py -d <direccion-deseada> -n <nombre-del-reporte>")
    parser.add_option("-n", "--nombre",
                      dest="nombre",
                      help="Nombre del archivo. Default: reporte.pdf")
    parser.add_option("-f", "--firmar",
                      dest="firmar",
                      help="Especifica si se desea mandar a firmar el archivo con MIFIEL Sandbox (https://app-sandbox.mifiel.com). Default: si|[no]")
    (options, args) = parser.parse_args()

    return options, args


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