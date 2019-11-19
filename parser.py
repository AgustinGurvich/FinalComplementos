import argparse

parser = argparse.ArgumentParser()

#Parametro obligatorio y posicional
parser.add_argument("file_name", help = "El nombre del archivo donde esta el grafo")

#Parametro opcional
parser.add_argument("--verbosity", help = "Activa la verbosidad", action = "store_true")

#Parametro opcional
parser.add_argument("-v", help = "Activa la verbosidad", action = "store_true")


args = parser.parse_args()
if args.verbosity:
    print("Activaste la verbosidad")
if args.v:
    print("Activaste la verbosidad")
print("Trataste de abrir "+args.file_name)
