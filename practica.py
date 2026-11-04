"""
Practica3

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México


Nombre del alumno: Osmar Ediel Armenta Medina
Número de control: 23212178
Correo institucional: l23212178@tectijuana.edu.mx


Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
import numpy as np
import math as m
import control as ctrl
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd

# Datos generales de la simulación

x0,t0,tend,dt,w,h = 0,0,15,1E-3,10,5
N = round((tend-t0)/dt) + 1
t = np.linspace(t0,tend,N)


# Componentes del circuito RLC
def sistema(R,C1,C2):
    num = [R*C2,(1-0.25)]
    den = [R*(C1+C2),1]
    sys = ctrl.tf(num,den)
    L = np.roots(den)
    return sys,L

#Control
R,C1,C2 = 100,100E-6,10E-6
syscontrol,L = sistema(R,C1,C2)
print(f'Funcion de transferencia del control: {syscontrol}')
print(f"Polos del sistema: L1 = {L[0]:.3e}\n")
#Caso
R,C1,C2 = 10E3,100E-6,10E-6
syscaso,L = sistema(R,C1,C2)
print(f'Funcion de transferencia del caso: {syscaso}')
print(f"Polos del sistema: L1 = {L[0]:.3e}\n")

# Componentes del controlador
def controlador(kP,kI,sys):
    numPI = [kP,kI]
    denPI = [1,0]
    PI = ctrl.tf(numPI,denPI)
    sysPI = ctrl.feedback(ctrl.series(PI,sys),1,sign=-1)
    return sysPI

# Controlador del Caso
casoPI = controlador(0.02149,3714.6075,syscaso)
print(f'Funcion de transferencia del caso en lazo cerrado: {casoPI}')

# Respuesta: Pulso unitario
F = np.zeros(N)
F[(t>=1) & (t<2)] = 1
_,Fsx = ctrl.forced_response(syscontrol,t,F,x0)
_,Fsy = ctrl.forced_response(syscaso,t,F,x0)
_,PID = ctrl.forced_response(casoPI,t,Fsx,x0)

#Colores
clr1 = np.array([9,21,64])/255
clr2 = np.array([118,146,255])/255
clr3 = np.array([171,210,250])/255
clr4 = np.array([250,150,50])/255

# Funciones del sistema en lazo abierto y lazo cerrado

def openloop(t,ft,):
    _,La = ctrl.forced_response(ft,t,x0)
    return La
def closedloop(t,ftPID,PpN):
    _,Lc = ctrl.forced_response(ftPID,t,PpN,x0)
    return Lc

#Respuestas

plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']

fg1 = plt.figure(1,figsize=(w,h))

plt.plot(t,F,'-',linewidth=1.5,color=clr1,label='F(t)')
plt.plot(t,Fsx,'-',linewidth=1.5,color=clr2,label='F(t): control')
plt.plot(t,Fsy,'--',linewidth=1.5,color=clr3,label='F(t): Caso')
plt.plot(t,PID,'--',linewidth=1.5,color=clr4,label='PID(t): Tratamiento')

plt.grid(False)
plt.xlim(0,10)
plt.xticks(np.arange(0,11,1))
plt.ylim(-0.1,1.1)
plt.yticks(np.round(np.arange(-0.1,1.11,0.1),1))

plt.xlabel('t [s]')
plt.ylabel('F(t) [V]')

plt.legend(bbox_to_anchor=(0.5,1.08),loc='center',ncol=4,frameon=False)

fg1.savefig('impulso_unitario_python.pdf',bbox_inches='tight')
plt.show()