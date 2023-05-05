<h1 align="center">Roomba</h1>

En este [repositorio](https://github.com/Diegodesantos1/Cena_de_los_filosofos) quedan resuelta la práctica de la cena de los filósofos

El código empleado para resolverlo es el siguiente:

<h2 align="center">Filósofos</h2>

```python
import time
import random
import threading
from tkinter import END
N = 5
TIEMPO_TOTAL = 3


class filosofo(threading.Thread):
    semaforo = threading.Lock()  # SEMAFORO BINARIO ASEGURA LA EXCLUSION MUTUA
    estado = []  # PARA CONOCER EL ESTADO DE CADA FILOSOFO
    tenedores = []  # ARRAY DE SEMAFOROS PARA SINCRONIZAR ENTRE FILOSOFOS, MUESTRA QUIEN ESTA EN COLA DEL TENEDOR
    count = 0

    def __init__(self, ventana):
        super().__init__()  # HERENCIA
        filosofo.semaforo.acquire()  # Bloqueo con el semáforo
        self.id = filosofo.count  # DESIGNA EL ID AL FILOSOFO
        self.comida = 0
        self.vent = ventana

        self.vent.labels[self.id].config(bg="white")
        filosofo.count += 1  # AGREGA UNO A LA CANT DE FILOSOFOS
        # EL FILOSOFO ENTRA A LA MESA EN ESTADO PENSANDO
        filosofo.estado.append('PENSANDO')
        # AGREGA EL SEMAFORO DE SU TENEDOR( TENEDOR A LA IZQUIERDA)
        filosofo.tenedores.append(threading.Semaphore(0))
        self.vent.escribe("El filósofo {0} está pensando".format(self.id))
        filosofo.semaforo.release()  # Libero el semáforo

    def pensar(self):
        # CADA FILOSOFO SE TOMA DISTINTO TIEMPO PARA PENSAR, ALEATORIO
        time.sleep(random.randint(0, 5))

    def derecha(self, i):
        return (i-1) % N  # BUSCAMOS EL INDICE DE LA DERECHA

    def izquierda(self, i):
        return(i+1) % N  # BUSCAMOS EL INDICE DE LA IZQUIERDA

    def verificar(self, i):
        if filosofo.estado[i] == 'HAMBRIENTO' and filosofo.estado[self.izquierda(i)] != 'COMIENDO' and filosofo.estado[self.derecha(i)] != 'COMIENDO':
            filosofo.estado[i] = 'COMIENDO'
            # SI SUS VECINOS NO ESTAN COMIENDO AUMENTA EL SEMAFORO DEL TENEDOR Y CAMBIA SU ESTADO A COMIENDO
            filosofo.tenedores[i].release()

    def tomar(self):
        time.sleep(2)
        filosofo.semaforo.acquire()  # SEÑALA QUE TOMARA LOS TENEDORES (EXCLUSION MUTUA)
        filosofo.estado[self.id] = 'HAMBRIENTO'
        self.vent.labels[self.id].config(bg="cyan")
        # VERIFICA SUS VECINOS, SI NO PUEDE COMER NO SE BLOQUEARA EN EL SIGUIENTE ACQUIRE
        self.verificar(self.id)
        # SEÑALA QUE YA DEJO DE INTENTAR TOMAR LOS TENEDORES (CAMBIAR EL ARRAY ESTADO)
        filosofo.semaforo.release()
        # SOLO SI PODIA TOMARLOS SE BLOQUEARA CON ESTADO COMIENDO
        filosofo.tenedores[self.id].acquire()

    def soltar(self):
        filosofo.semaforo.acquire()  # SEÑALA QUE SOLTARA LOS TENEDORES
        filosofo.estado[self.id] = 'PENSANDO'
        self.vent.escribe("El filósofo {} está pensando".format(self.id))
        self.vent.labels[self.id].config(bg="white")
        self.verificar(self.izquierda(self.id))
        self.verificar(self.derecha(self.id))
        filosofo.semaforo.release()  # YA TERMINO DE MANIPULAR TENEDORES

    def comer(self):
        self.vent.tenedores[self.id].config(bg="orange")
        self.vent.tenedores[(self.id-1) % N].config(bg="orange")
        print("El filósofo {} coge el tenedor {} y {}".format(
            self.id, self.id, (self.id+1) % N))

        self.vent.escribe("El filósofo {} está comiendo".format(self.id))

        self.vent.labels[self.id].config(bg="gold")
        self.vent.tenedores[self.id].config(bg="orange", fg="white")
        self.vent.tenedores[(self.id-1) % N].config(bg="orange", fg="white")
        time.sleep(4)  # TIEMPO PARA COMER
        self.vent.escribe("El filósofo {} terminó de comer".format(self.id))

        print("El filósofo {} suelta el tenedor {} y {}".format(
            self.id, self.id, (self.id+1) % N))
        self.vent.tenedores[self.id].config(bg="orange", fg="white")
        self.vent.tenedores[(self.id-1) % N].config(bg="orange", fg="white")

        self.comida += 1
        self.vent.caja[self.id].delete(0, END)
        self.vent.caja[self.id].insert(0, self.comida)

    def run(self):
        self.vent.labels[self.id].config(bg="pink")
        for i in range(random.randint(1, 5)):
            self.pensar()  # EL FILOSOFO PIENSA
            self.tomar()  # AGARRA LOS TENEDORES CORRESPONDIENTES
            self.comer()  # COME
            self.soltar()  # SUELTA LOS TENEDORES
            self.vent.labels[self.id].config(bg="pale green")
        self.vent.escribe("El filósofo {} ha terminado".format(self.id))
        self.vent.labels[self.id].config(bg="red")
```

***

<h2 align="center">Interfaz Gráfica</h2>

```python
import tkinter as tk
from filosofos import *
import math


class Ventana():
    def __init__(self):
        self.root = tk.Tk()
        alto = 35
        ancho = 60
        self.root.title("La cena de los filósofos")
        self.root.geometry("1280x720")
        self.fondo = "light grey"
        self.root.configure(bg=self.fondo)
        self.text = tk.Text(self.root, height=alto, width=ancho)
        self.scroll = tk.Scrollbar(self.root)
        self.caja = []
        self.labels = []
        self.tenedores = []
        self.añadirCaja()
        self.text.configure(yscrollcommand=self.scroll.set)
        self.text.place(x=10, y=160, height=500, width=500)
        self.scroll.config(command=self.text.yview)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        tk.Label(self.root, text="Leyenda ", font='System 18 bold',
                 bg=self.fondo).place(x=475, y=0)
        tk.Label(self.root, text=" ", bg="pink").place(x=125, y=40)
        tk.Label(self.root, text="El Filósofo entra a comer",
                 bg=self.fondo).place(x=140, y=40)
        tk.Label(self.root, text=" ", bg="cyan").place(x=125, y=65)
        tk.Label(self.root, text="El filósofo tiene hambre",
                 bg=self.fondo).place(x=140, y=65)
        tk.Label(self.root, text=" ", bg="gold").place(x=125, y=90)
        tk.Label(self.root, text="El filósofo está comiendo",
                 bg=self.fondo).place(x=140, y=90)
        tk.Label(self.root, text=" ", bg="pale green").place(x=350, y=40)
        tk.Label(self.root, text="El filósofo terminó",
                 bg=self.fondo).place(x=365, y=40)
        tk.Label(self.root, text=" ", bg="white").place(x=350, y=65)
        tk.Label(self.root, text="El filósofo está pensando",
                 bg=self.fondo).place(x=365, y=65)
        tk.Label(self.root, text=" ", bg="red").place(x=350, y=90)
        tk.Label(self.root, text="El filósofo se levanta",
                 bg=self.fondo).place(x=365, y=90)
        tk.Label(self.root, text=" ", bg="orange").place(x=585, y=40)
        tk.Label(self.root, text="Tenedor ocupado",
                 bg=self.fondo).place(x=600, y=40)
        tk.Label(self.root, text=" ", bg="light green").place(x=585, y=65)
        tk.Label(self.root, text="Tenedor libre",
                 bg=self.fondo).place(x=600, y=65)
        tk.Label(self.root, text="Número de comidas",
                 font='System 16 bold', bg=self.fondo).place(x=600, y=110)

    def añadirCaja(self):
        angulo = math.pi/N
        for i in range(N):
            cajaaux = tk.Entry(self.root)
            cajaaux.place(x=700, y=140+i*20)
            tk.Label(self.root, text="Filósofo "+str(i)+":",
                     bg=self.fondo).place(x=600, y=140+i*20)
            label = tk.Label(self.root, text="Filósofo "+str(i))
            label2 = tk.Label(self.root, text="Ten. " + str(i))
            label2.config(bg="grey", fg="white")
            label.place(x=700+100*math.cos(2*angulo*i),
                        y=400+100*math.sin(2*angulo*i))
            label2.place(x=700+100*math.cos(angulo*(2*i+1)),
                         y=400+100*math.sin(angulo*(2*i+1)))
            self.caja.append(cajaaux)
            self.labels.append(label)
            self.tenedores.append(label2)

    def escribe(self, texto):
        self.text.insert(tk.END, str(texto)+"\n")
        print(str(texto))
        self.text.see(tk.END)

    def run(self):
        self.root.mainloop()
```

***

<h2 align="center">Main</h2>

```python
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
```

****

<h2 align="center">Resultado</h2>

Este es el resultado final:

![image](https://user-images.githubusercontent.com/91721855/236356878-80e9e770-6967-4050-a63e-35abcd58c033.png)
