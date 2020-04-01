from generator import ReportGenerator
from optparse import OptionParser

def main():
    get_input = input_options()

    options = get_input[0]
    arguments = get_input[1]

    direccion = options.direccion
    nombre = options.nombre

    generador = ReportGenerator()
    generador.reporte(direccion, nombre)

def input_options():
    parser = OptionParser(usage="\n\nUso: gestor.py -d <direccion-deseada> -n <nombre-del-reporte>")
    parser.add_option("-d", "--direccion",
                      dest="direccion",
                      help="Direccion del reporte a generar")
    parser.add_option("-n", "--nombre",
                      dest="nombre",
                      help="Nombre del archivo. Default: reporte.pdf")
    (options, args) = parser.parse_args()

    return options, args


if __name__ == '__main__':
    main()
