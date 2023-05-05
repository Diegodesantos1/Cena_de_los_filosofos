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
