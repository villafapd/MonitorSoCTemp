
import os
import threading
import time
#import tkinter as Disp
from gpiozero import *
from tkinter import * 
from tkinter import messagebox
import sys
import time
import wiringpi

# One of the following MUST be called before using IO functions:
wiringpi.wiringPiSetup()      # For sequential pin numbering
wiringpi.pinMode (5, 1) # Salida PIN 5 , 1 es salida

# OR
wiringpi.wiringPiSetupSys()   # For /sys/class/gpio with GPIO pin numbering
# OR
wiringpi.wiringPiSetupGpio()  # For GPIO pin numbering

Temp_SoC = 0
Temp_Float = 0
Cooler = LED(5)
Str_Float = "0"
Ventilador = "Apagado"
ColorFondo = "grey"
FirstScan = 0
previousMillis = 0


#---------------------------------------------------------------------------------------------   
# Declaración de Funciones
#---------------------------------------------------------------------------------------------   
def LogicaCtrlCPU():
    cpu_temp = os.popen("vcgencmd measure_temp").readline()
    cpu_temp1= cpu_temp.replace("temp=", "")
    longStr = len(cpu_temp1)
    global Str_Float
    Str_Float = cpu_temp1[0:longStr-3]
    Temp_Float = float(Str_Float)
    #print("Temperatura actual SoC: " + Str_Float + " °C")
    global Ventilador
    global ColorFondo
    if Temp_Float >= 60.0:
     #   print("Alarma Alta Temperatura SoC")
        Cooler.on() #El programa actual tiene esta salida invertida por el tipo de rele
        if wiringpi.digitalRead(5)==1:
            Ventilador= "Encendido" #+ str(wiringpi.digitalRead(5)) 
            ColorFondo = "green"

    if Temp_Float <= 40:#39.0:
      #  print("Alarma Baja Temperatura SoC")
        Cooler.off()
        if wiringpi.digitalRead(5)==0:
            Ventilador="Apagado  "
            ColorFondo = "grey"
    lblNum2 = Label(VentanaPrincipal,text= Str_Float+ " °C")
    lblNum2.grid(row=0,column=0,padx=130, pady=6, sticky="w",ipady=6)
    lblNum4 = Label(VentanaPrincipal,text=Ventilador,bg=ColorFondo)  
    lblNum4.grid(row=1,column=0,padx=110, pady=6, sticky="w",ipady=6 )  
    #VentanaPrincipal.update_idletasks()
    #VentanaPrincipal.update()

def endProgram():
    MsgBox = messagebox.askquestion ('Salir Aplicación','Seguro quiere salir?',icon = 'error')
    if MsgBox == 'yes':
        VentanaPrincipal.quit()
        VentanaPrincipal.destroy()
        sys.exit()
    else:
        messagebox.showinfo('Bienvenido de vuelta','Retorno a la Aplicación')

#---------------------------------------------------------------------------------------------   
#Carga de configuracion de tkinter
#---------------------------------------------------------------------------------------------
VentanaPrincipal = Tk() #Display.Tk()
VentanaPrincipal.title("Monitor Temperatura Procesador")
VentanaPrincipal.geometry("200x120")
lblNum1 = Label(VentanaPrincipal,text="Temp. Procesador: ")
lblNum1.grid(row=0,column=0,padx=6, pady=6, sticky="w",ipady=6)
lblNum2 = Label(VentanaPrincipal,text= Str_Float+ " °C")
lblNum2.grid(row=0,column=0,padx=130, pady=6, sticky="w",ipady=6)
lblNum3 = Label(VentanaPrincipal,text="Estado Cooler: ")
lblNum3.grid(row=1,column=0,padx=6, pady=6, sticky="w",ipady=6 )
lblNum4 = Label(VentanaPrincipal,text=Ventilador,bg=ColorFondo)  
lblNum4.grid(row=1,column=0,padx=110, pady=6, sticky="w",ipady=6 )  

Boton1 = Button(VentanaPrincipal, text = "Salir", command=endProgram)
Boton1.place(x=130, y=85)
VentanaPrincipal.resizable(width=False, height=False)
VentanaPrincipal.protocol("WM_DELETE_WINDOW",endProgram)

#---------------------------------------------------------------------------------------------   
#Loop
#---------------------------------------------------------------------------------------------   

if __name__ == "__main__":
     
    while True:
        currentMillis = int(round(time.time() * 1000)) 
        #print (currentMillis)
        if currentMillis - previousMillis >=5000:
        #print(currentMillis - previousMillis)
        #print(previousMillis)
            LogicaCtrlCPU()
            previousMillis = currentMillis
    
        VentanaPrincipal.update_idletasks()
        VentanaPrincipal.update()
        



 




    


        

        
   
