#!/usr/bin/python

# Programa em interface gráfica como 
# demonstração da aplicação de modelos
# matemáticos na resolução de 
# problemas comuns à engenharia

from scipy.integrate import odeint 

import sympy as sym
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk

from tkinter import *

sym.init_printing(use_unicode=True)


# Symbolic expressions and data
def sym_tank():

    def tank(Q, t, Fin, Fout, Cin, V):
        return Fin*Cin - Fout*(Q/V)

    # Leitura dos dados dos campos de parâmetros
    Fin   = float(Fin_entry.get()  )
    Fout  = float(Fout_entry.get() )
    Cin   = float(Cin_entry.get()  )
    V     = float(Vol_entry.get()  )
    ftime = float(ftime_entry.get())
    Q0    = float(Q0_entry.get()   )

    # Definição das viriáveis e funções símbolicas
    t = sym.symbols('t')
    Q = sym.Function('Q')(t)
    dQdt = Q.diff(t)
    expr = sym.Eq(Fin*Cin - Fout*(Q/V), dQdt)

    # Resolução da EDO e cálculo dos dados para plot
    t_range = np.arange(0, ftime, 1)
    F = sym.dsolve(expr, ics={Q.subs(t,Q0):0})
    y = odeint(tank, Q0, t_range, args=(Fin, Fout, Cin, V))

    # Retorno dos dados
    return (F, t_range, y)

def sym_reactor_batch():
    # Reação irreversível elementar do tipo A -> B
    X = sym.symbols('X')
    order = int(order_var.get())
    k     = float(k_entry.get())
    Cao   = float(Cao_entry.get())
    V     = float(batch_vol_entry.get())

    if(order == 1):
        exp = 1/(k*(1-X))
    elif(order == 2):
        exp = 1/(k*Cao) * (1/(1-X)**2)
    else:
        exp = 1/(k*(1-X))

    F = sym.integrate(exp,X)

    X_range = np.arange(0,1,0.01)
    t_range = [sym.re(exp.subs(X,x)) for x in X_range]
    
    return (F, X_range, t_range)

def sym_reactor_pfr():

    # Reação irreversível elementar do tipo 1A -> 1B

    # Leitura dos parâmetros
    X = sym.symbols("X")
    k = float(k_entry.get())
    v = float(flux_entry.get())
    Cao = float(Cao_entry.get())
    order = float(order_var.get())

    # Determinação da expressão segundo a 
    # ordem da reação selecionada
    if(order == 1):
        exp =(v/k) * (1/(1-X))
    elif (order == 2):
        exp = (v/Cao*k) * (1/(1-X)**2)

    # Resolução da integral simbólica
    F = sym.integrate(exp, X)
    X_range = np.arange(0, 1, 0.01)
    v_range = [sym.re(F.subs(X,x)) for x in X_range]

    return (F, X_range, v_range)

def sym_circuits():

    def circuits(I, t, E, R, L):
        return (E-(R*I))/L

    # Leitura dos dados dos campos de entrada de parâmetros
    E  = float(tension_entry.get())
    R  = float(resist_entry.get())
    I0 = float(init_curr_entry.get())
    L  = float(induction_entry.get())
    tf = float(time_range_entry.get())

    # Declaração das variáveis e funções simbólicas
    t = sym.symbols('t')
    I = sym.Function('I')(t)
    dIdt = sym.diff(I,t)
    exp  = sym.Eq((E-(R*I))/L, dIdt)
    
    # Resolução via sym.dsolve
    F = sym.dsolve(exp, ics={I.subs(t,0):I0})
    
    # Resolução da EDO via scipy.odeint
    t_range = np.arange(0,tf,0.01)
    sol = odeint(circuits, I0, t_range, args=(E,R,L))
    
    # Retorno dos dados
    return (F, t_range, sol)

def sym_circuits_2():

    def circuits_2(I,t):
        return 2*np.sin(t) - 20*I

    t = sym.symbols('t')
    I = sym.Function('I')(t)
    I0 = float(init_curr_entry.get())
    tf = float(time_range_entry.get())
    
    dIdt = sym.diff(I,t)
    exp = sym.Eq(2*sym.sin(t) - 20*I, dIdt)
    F = sym.dsolve(exp, ics={I.subs(t,0):I0})

    t_range = np.arange(0, tf, 0.01)
    sol = odeint(circuits_2, I0, t_range)
#   y = [F.subs(t,x).rhs for x in t_range]

    return (F, t_range, sol)


# Clear frame
def clearframe(frame):
    for widget in frame.winfo_children():
        widget.destroy()


# Set data for the widgets
def set_data():
    def set_formula(exp):
        exp_label=Label(app, text=exp, background=formula_bg, foreground="#FFFFFF")
        exp_label.place(x=wpos["exp"][0], y=wpos["exp"][1], width=wpos["exp"][2], height=wpos["exp"][3])

    def plot(data, x_label, y_label):
        clearframe(result_label)
        figure = plt.Figure(figsize=(5,4), dpi=80)
        figure.add_subplot(111, xlabel=x_label, ylabel=y_label).plot(data[0],data[1])
        chart = FigureCanvasTkAgg(figure, result_label)
        NavigationToolbar2Tk(chart, result_label)
        chart.draw()
        chart.get_tk_widget().pack(fill="both", expand=True)

    models = {
        "tank"      :(sym_tank          ,"time(min)"    ,"mass(g)"    ),
        "pfr"       :(sym_reactor_pfr   ,'conversão(X)' ,'volume(dm³)'),
        "batch"     :(sym_reactor_batch ,'conversão(X)' ,"tempo(min)" ),
        "circuits"  :(sym_circuits      ,'tempo(min)'   ,'corrente(A)'),
        "circuits_2":(sym_circuits_2    ,'tempo(min)'   ,'corrente(A)')
    }

    model   = model_var.get()

    data    = models[model][0]()
    label_x = models[model][1]
    label_y = models[model][2]

    set_formula(data[0])
    plot(data[1::],label_x, label_y)

# Set model to use
def set_model(model):
    
    clearframe(params)
    draw_model_switcher()
    model_var.set(model)

    if(model == "batch" or model == "pfr"):
        draw_reactor_parameters(model)
        return
    if(model == "tank"):
        draw_tank_widgets() 
        return
    if(model == "circuits" or model == "circuits_2"):
        draw_circuits_parameters()
        return


# Widgets
def draw_header(header_title):
    global header
    header = Label(app, 
    text=header_title, borderwidth=2, relief="groove",
    font=("Arial Black",20), background=header_bg, foreground="#FFFFFF")
    header.place(x=wpos["header"][0], y=wpos["header"][1], width=wpos["header"][2], height=wpos["header"][3])

def draw_tank_widgets():
    draw_header("Massa de sal em tanque")
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

def draw_reactor_parameters(model):
    global Cao_entry, k_entry, batch_vol_entry, flux_entry

    reactor_type = {"batch":"batelada","pfr":"pfr"} 
    draw_header("Tempo de reação no reator {}".format(reactor_type[model]))

    global Cao_entry, k_entry, batch_vol_entry, flux_entry, order_var
    
    Cao_label = Label(params, text="Concentração inicial", background=labels_bg, foreground="#FFFFFF", anchor="w")
    Cao_label.place(x=10,y=85,width=290, height=20)
    Cao_entry = Entry(params)
    Cao_entry.place(x=10,y=115, width=290, height=20)

    k_label = Label(params, text="Velocidade específica da reação", background=labels_bg, foreground="#FFFFFF", anchor="w")
    k_label.place(x=10, y=145, width=290, height=20)
    k_entry = Entry(params)
    k_entry.place(x=10, y=175, width=290, height=20)

    batch_vol_label = Label(params, text="Volume do batelada", background=labels_bg, foreground="#FFFFFF", anchor="w")
    batch_vol_label.place(x=10, y=205, width=290, height=20)
    batch_vol_entry = Entry(params)
    batch_vol_entry.place(x=10, y=235, width=290, height=20)

    flux_label = Label(params, text="Vazão volumétrica", background=labels_bg, foreground="#FFFFFF", anchor="w")
    flux_label.place(x=10, y=265, width=290, height=20)
    flux_entry = Entry(params)
    flux_entry.place(x=10,y=295, width=290, height=20)

    order_var = StringVar()
    order_label = Label(params, text="Ordem da reação", background=labels_bg, foreground="#FFFFFF", anchor="w")
    order_label.place(x=10,y=325, width=290, height=20)
    
    order_radio_1 = Radiobutton(params, text="1ª", value=1, variable=order_var)
    order_radio_2 = Radiobutton(params, text="2ª", value=2, variable=order_var)
    order_radio_3 = Radiobutton(params, text="3ª", value=3, variable=order_var)

    order_radio_1.place(x=10, y=365, width=60, height=20)
    order_radio_2.place(x=80, y=365, width=60, height=20)
    order_radio_3.place(x=150, y=365, width=60, height=20)

def draw_circuits_parameters():
    draw_header("Corrente em um circuito")
    
    global tension_entry, resist_entry, init_curr_entry, induction_entry, time_range_entry
    
    tension_label = Label(params, text="Tensão inicial", background=labels_bg, foreground="#FFFFFF",anchor="w")
    tension_label.place(x=10,y=85,width=290, height=20)
    tension_entry = Entry(params)
    tension_entry.place(x=10, y=115, width=290, height=20)

    resist_label = Label(params, text="Resistência(ohms)", background=labels_bg, foreground="#FFFFFF", anchor="w")
    resist_label.place(x=10,y=145, width=290, height=20)
    resist_entry = Entry(params)
    resist_entry.place(x=10, y=175, width=290, height=20)

    init_curr_label = Label(params, text="Corrente inicial (A)", background=labels_bg, foreground="#FFFFFF", anchor="w")
    init_curr_label.place(x=10,y=205, width=290, height=20)
    init_curr_entry = Entry(params)
    init_curr_entry.place(x=10, y=235, width=290, height=20)

    induction_label = Label(params, text="Indutância(H)", background=labels_bg, foreground="#FFFFFF", anchor='w')
    induction_label.place(x=10, y=265, width=290, height=20)
    induction_entry = Entry(params)
    induction_entry.place(x=10, y=295, width=290, height=20)

    time_range_label = Label(params, text="Intervalo de integração (min)", background=labels_bg, foreground="#FFFFFF", anchor='w')
    time_range_label.place(x=10, y=325, width=290, height=20)
    time_range_entry = Entry(params)
    time_range_entry.place(x=10, y=355, width=290, height=20)


# Windows
def aboutMe():
    about = Tk()
    about.title("Sobre")
    app.geometry("300x300")
    title = Label(about, text="Model Visualizer",font=("Arial Bold",12))
    title.place(x=10, y=10, width=280, height=50)
    content = Label(about, text="Programa desenvolvido para o processo\n trainee da CodeQ em 2022/2")
    content.place(x=10,y=70, width=280, height=50)
    autors = Label(about, text="Autores:\nEstêvão Mendes Santana\nYuri Mewius\nVítor Soares Gonçalves")
    autors.place(x=10, y=130, width=280, height=90)
    year_label = Label(about, text="Universidade Federal de Santa Maria\nOutubro de 2022")
    year_label.place(x=10, y=230, width=280, height=35)
    about.mainloop()

def main_app():
    global app
    app = Tk()
    app.title("Modelagem computacional")
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

def draw_model_switcher():
    # Model switch
    global model_var, model, model_entry
    model_var = StringVar()
    models = ["tank", "batch", "pfr", "circuits", "circuits_2"]
    
    model  = Label(params, text="Modelo",background=labels_bg, foreground="#FFF", anchor="w")
    model.place(x=10, y=40, width=50, height=20)
    
    model_entry  = OptionMenu(params, model_var, *models, command=set_model)
    model_entry.place(x=60, y=40, width=75, height=30)


# Main Widgets
def draw_main_widgets():
    global exp_label, result_label, params
    
    b_width = 3
    b_type = "groove"

    # Frames 
    # title_header = Frame(app)
    # title_header.place()

    # formula_frame = Frame(app)
    # formula_frame.place()

    # plot_frame = Frame(app)
    # plot_frame.place()

    # model_switcher = Frame(app)
    # model_switcher.place()

    # params_frame = Frame(, background="", foreground="")
    # params_frame.place(x=,y=,width=,height=)

    # button_frame = Frame(app)
    # button_frame.place()
    
    # Labels
    exp_label=Label(app, text="Fórmula", background="#570091", foreground="#FFFFFF", borderwidth=b_width, relief=b_type)
    exp_label.place(x=wpos["exp"][0], y=wpos["exp"][1], width=wpos["exp"][2], height=wpos["exp"][3])
    
    result_label=Label(app, text="Plot", background="#9a34cc", foreground="#FFF", borderwidth=b_width, relief=b_type)
    result_label.place(x=wpos["res"][0], y=wpos["res"][1], width=wpos["res"][2], height=wpos["res"][3])
    
    params=Label(app, text="Parameters", background=labels_bg, foreground="#FFF", anchor="n", borderwidth=b_width, relief=b_type)
    params.place(x=wpos["params"][0], y=wpos["params"][1], width=wpos["params"][2], height=wpos["params"][3])
    
    Button(app,text="Calcular",command=set_data).place(
    x=wpos["button"][0], y=wpos["button"][1], width=wpos["button"][2], height=wpos["button"][3])


# Widgets colors
header_bg  = "#570091"
labels_bg  = "#6400cd"
formula_bg = "#570091"
result_bg  = "#9A34CC"

# Widgets measurements
wpos = {
   "header": [10,  10,  810, 50 ],
   "exp"   : [10,  70,  480, 50 ],
   "res"   : [10,  130, 480, 470],
   "params": [510, 70,  310, 470],
   "button": [510, 550, 310, 40 ]
}

main_app()
draw_main_widgets()
set_model("tank")

app.mainloop()