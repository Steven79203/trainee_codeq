#!/usr/bin/python

# Projeto Trainee CodeQ 2022/2

# Programa em interface gráfica como 
# demonstração da aplicação de modelos
# matemáticos na resolução de 
# problemas comuns à engenharia

"""
    TODO:
        > GUI
        > Mostrar o plot dos modelos
        > Mostrar a expressão - OK
        > Espaços para inserção dos parâmetros no modelo
"""

# 1 - Massa de sal em um tanque
from matplotlib import gridspec
from scipy.integrate import odeint 
from scipy.integrate import quad

import sympy as sym
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tkinter import *

sym.init_printing(use_unicode=True)

def plot(data):
    figure = plt.Figure(figsize=(5,4), dpi=80,)
    figure.add_subplot(111, xlabel="time(min)", ylabel="mass (g)").plot(data[0],data[1])
    chart = FigureCanvasTkAgg(figure, result_label)
    chart.draw()
    chart.get_tk_widget().place(x=-1,y=-1,width=480,height=480)

def tank():
    
    Fin, Fout, Cin, V = 3, 3, 2, 300
    def dQdt(Q,t, Fin, Fout, Cin):
        return Fin*Cin - Fout*(Q/V)
    
    Fin  = float(input("Vazão de entrada (L/min): "))
    Fout = float(input("Vazão de saída (L/min): "))
    Cin  = float(input("Concentração na alimentação (g/L): "))
    V    = float(input("Volume do tanque (L): "))
    tf   = float(input("Tempo final de integração (min): "))

    ti = 0
    Q0 = float(input('Quantidade inicial de sal no tanque(g):'))

    t = np.arange(ti,tf,1)

    sol = odeint(dQdt, Q0, t, args=(Fin, Fout, Cin))

    plt.plot(t, sol, label='massa de sal')
    plt.legend()
    plt.grid()
    plt.xlabel('t (min)')
    plt.ylabel('m (g)')
    plt.show()

def tank_function():
    def dQdt(Q,t, Fin, Fout, Cin):
        return Fin*Cin - Fout*(Q/V)
    
    Fin  = float(Fin_entry.get())
    Fout = float(Fout_entry.get())
    Cin  = float(Cin_entry.get())
    V    = float(Vol_entry.get())
    Q0   = float(Q0_entry.get())
    tf   = int(ftime_entry.get())

    t = np.arange(0,tf,1)

    sol = odeint(dQdt, Q0, t, args=(Fin, Fout, Cin))
    return (t, sol)

# 2.1 - Reator batelada - Reação de 1ª Ordem
def batch_reactor():
    def first(X, k):
        return 1/(k*(1-X))

    k = 0.1
    V = quad(first, 0, 0.8, args=(k))
    print(V)

# 2.2 - Reatores contínuos
def cont_reactors(order="first"):
    def first(X, v, k, Cao):
      return (v/k*Cao) * (1/(1-X))

    def second(X, v, k, Cao):
      return 

    def third(X, v, k, Cao):
      pass

    k   = 1  # Velocidade específica da reação
    Cao = 1  # Concentração inicial
    v   = 1   # Vazão volumétrica

    if(order == "first"):
        V = quad(first, 0, 0.8, args=(v, k, Cao))
        return
    if(order == "second"):
        V = quad(second, 0, 0.8, args=(k, Cao))
        return
    if(order == "third"):
        V = quad(third, 0, 0.8, args=(k, Cao))
        return


# Symbolic Formulas
def sym_tank():
    Fin = float(Fin_entry.get())
    Fout = float(Fout_entry.get())
    Cin = float(Cin_entry.get())
    V = float(Vol_entry.get())

    t = sym.symbols('t')
    Q = sym.Function('Q')(t)
    dQdt = Q.diff(t)
    expr = sym.Eq(Fin*Cin - Fout*(Q/V), dQdt)

    F = sym.dsolve(expr, ics={Q.subs(t,0):0})
    return F

def sym_reactor_batch():
    X = sym.symbols('X')

    k = 0.01
    exp = 1/(-k*(1-X))
    return sym.integrate(exp,X)

def sym_reactor_pfr():
    X = sym.symbols("X")

    k = 0.01
    v = 10
    exp = (v/k) * (1/(1-X))
    return sym.integrate(exp,X)

def sym_circuits():
    pass


def set_formula(function):
    exp_label=Label(app, text=function(), background=formula_bg, foreground="#FFFFFF")
    exp_label.place(x=wpos["exp"][0], y=wpos["exp"][1], width=wpos["exp"][2], height=wpos["exp"][3])

def set_result(function):
    result_label = Label(app, text="Result = {:2.2f} gramas de sal".format(function()), background=result_bg, foreground="#FFF")
    result_label.place(x=wpos["res"][0],y=wpos["res"][1], width=wpos["res"][2], height=wpos["res"][3])
    ## TODO : Determine uma nova string posfixa para cada resultado


def get_data():
    model = model_entry.get()
    if(model == "tank"):
        set_formula(sym_tank)
        #set_result(tank_function, "gramas de sal")
        data = tank_function()
        # TODO: Também delimite uma área de plot
        plot(data)
    if(model == "pfr"):
        set_formula(sym_reactor_pfr)
    if(model == "batch"):
        set_formula(sym_reactor_batch)
    if(model == "circuit"):
        set_formula(sym_circuits)


def draw_tank_widgets():
# Fin
    global Fin_entry, Fout_entry, Cin_entry, Vol_entry, Q0_entry, ftime_entry
    Fin_label  = Label(params, text="Vazão de entrada(L/min)", background=labels_bg, foreground="#FFF", anchor="w")
    Fin_label.place(x=10,y=85, width=290, height=20)
    Fin_entry = Entry(params)
    Fin_entry.place(x=10,y=115, width=290, height=20)

    #Fout 
    Fout_label  = Label(params, text="Vazão de saída(L/min)", background=labels_bg, foreground="#FFF", anchor="w")
    Fout_label.place(x=10,y=155, width=290, height=20)
    Fout_entry  = Entry(params)
    Fout_entry.place(x=10,y=185, width=290, height=20)

    #Cin 
    Cin_label  = Label(params, text="Concentração de entrada (g/L)", background=labels_bg, foreground="#FFF", anchor="w")
    Cin_label.place(x=10,y=215, width=290, height=20)
    Cin_entry  = Entry(params)
    Cin_entry.place(x=10,y=245, width=290, height=20)

    # Volume
    Vol_label  = Label(params, text="Volume (L)", background=labels_bg, foreground="#FFF", anchor="w")
    Vol_label.place(x=10,y=275, width=290, height=20)
    Vol_entry  = Entry(params)
    Vol_entry.place(x=10,y=305, width=290, height=20)

    # Massa de sal inicial
    Q0_label  = Label(params, text="Quantidade inicial (g)", background=labels_bg, foreground="#FFF", anchor="w")
    Q0_label.place(x=10,y=335, width=290, height=20)
    Q0_entry  = Entry(params)
    Q0_entry.place(x=10,y=365, width=290, height=20)

    # Tempo final da integração
    ftime_label  = Label(params, text="Tempo final (min)", background=labels_bg, foreground="#FFF", anchor="w")
    ftime_label.place(x=10,y=395, width=290, height=20)
    ftime_entry  = Entry(params)
    ftime_entry.place(x=10,y=425, width=290, height=20)

def draw_reactor_widgets():
    pass

def draw_circuits_widgets():
    pass

def aboutMe():
    about = Tk()
    about.title("Sobre")
    app.geometry("300x250")
    title = Label(about, text="Programa Trainee CodeQ 2022/2",font=("Arial Bold",12))
    title.place(x=10, y=10, width=280, height=50)
    content = Label(about, text="Programa desenvolvido para o processo\n trainee da CodeQ em 2022/2")
    content.place(x=10,y=70, width=280, height=50)
    autors = Label(about, text="Autores:\nEstêvão Mendes\nYuri Mewius\nVítor")
    autors.place(x=10, y=130, width=280, height=90)
    about.mainloop()

app = Tk()
app.title("CodeQ Trainee Program")
app.geometry("1000x700")

menuBar = Menu(app)

menuFile = Menu(menuBar, tearoff=0)
menuFile.add_command(label="Fechar", command=app.quit)
menuBar.add_cascade(label="Arquivos", menu=menuFile)

menuAbout = Menu(menuBar, tearoff=0)
menuAbout.add_command(label="Ajuda")
menuAbout.add_command(label="Sobre", command=aboutMe)
menuBar.add_cascade(label="Sobre", menu=menuAbout)

app.config(menu=menuBar)
app.configure(background="#B9F")

# Common variables
header_bg  = ""
labels_bg  = "#6400cd"
formula_bg = "#570091"
result_bg  = "#9A34CC"

wpos = {
   "header": [10,  10, 810,  50],
   "exp"   : [10,  70, 480,  50],
   "res"   : [10,  130, 480, 470],
   "params": [510, 70, 310, 470],
   "button": [510, 550,310, 40]
}

# Cabeçalho
header = Label(app, 
            text="Programa Trainee CodeQ 2022/2", 
            borderwidth=2, relief="groove",
            font=("Arial Black",20), 
            background="#570091", foreground="#FFFFFF")
header.place(x=wpos["header"][0], y=wpos["header"][1], width=wpos["header"][2], height=wpos["header"][3])

# Formula label
exp_label=Label(app, text="Fórmula", background="#570091", foreground="#FFFFFF")
exp_label.place(x=wpos["exp"][0], y=wpos["exp"][1], width=wpos["exp"][2], height=wpos["exp"][3])
#exp_label.pack(ipadx=10, ipady=10, padx=10, pady=10, side='top', expand=True)

# Result label
result_label=Label(app, text="Resultado:", background="#9a34cc", foreground="#FFF")
result_label.place(x=wpos["res"][0], y=wpos["res"][1], width=wpos["res"][2], height=wpos["res"][3])
plot((0,0))
#result_label.pack(ipadx=10, ipady=10, padx=10, pady=10, side="left")

# Parameters label
params=Label(app, text="Parameters", background=labels_bg, foreground="#FFF", anchor="n")
params.place(x=wpos["params"][0], y=wpos["params"][1], width=wpos["params"][2], height=wpos["params"][3])
#txt3.pack(ipadx=10, ipady=10, padx=10, pady=10, side="right")

# Model switch
model  = Label(params, text="Modelo",background=labels_bg, foreground="#FFF", anchor="w")
model.place(x=10, y=25, width=290, height=20)
model_entry = Entry(params)
model_entry.place(x=10, y=55, width=290, height=20)

# TODO: Implement buttons to set each model to use
draw_tank_widgets()
Button(app,text="Calcular",command=get_data).place(
    x=wpos["button"][0], y=wpos["button"][1], width=wpos["button"][2], height=wpos["button"][3])

# Ao clicar botão
# Verificar qual evento chamar
# Se tanque ou reator ou circuitos
# Chame as devidas funções com os devidos parâmetros
# Retorne o resultado para os devidos labels/txts

# TODO:
    # Create plot region
    # Create parameter controls 
    # Expression visualization
app.mainloop()