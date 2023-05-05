from interfaz import Ventana
from filosofos import N, filosofo

if __name__ == "__main__":
    V = Ventana()

    lista = []
    for i in range(N):
        lista.append(filosofo(V))

    for f in lista:
        f.start()
    V.run()
    for f in lista:
        f.join()
