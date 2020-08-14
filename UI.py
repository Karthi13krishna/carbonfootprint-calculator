import tkinter as tk
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

a = [0,0,0,0]

def button_pressed():
    a[0] = calc(elec_entry.get(),0.708)
    a[1] = calc(bus_entry.get(),0.10312)
    a[2] = calc(local_train_entry.get(),0.036939994)
    a[3] = calc(train_entry.get(),0.00497)
    final_text.set("{:.2f}".format(sum(a)/1000) + " metric tons of CO2")
    
    y_label = tk.Label(tab3, text = "kg of CO2", padx = 10, pady =10)
    y_label.grid(row = 0, column = 0)
    
    b = ['Electricity','Bus','Local Train','Train']
    f = Figure(figsize=(4,3), dpi=100)
    ax = f.add_subplot(111).bar(b,a)
    
    result_bar = FigureCanvasTkAgg(f, tab3)
    result_bar.get_tk_widget().grid(row = 0, column = 1, padx = 30, pady = 30)
    tabControl.select(2) 
    
def selec():
    tabControl.select(1)
       
def calc(var, val):
    try:
        carbon = (float(var) * val)
    except:
        carbon = 0
    return carbon

root = tk.Tk()
style = ThemedStyle(root)
style.set_theme("plastik")
root.title("CarbonFootprint Calculator")
root.geometry("640x480")

tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl) 
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)

tabControl.add(tab1, text ='House') 
tabControl.add(tab2, text ='Transport')
tabControl.add(tab3, text = 'Result')
style.configure("Tab", focuscolor=style.configure(".")["background"])
tabControl.pack(expand = 1, fill ="both")

elec_label = tk.Label(tab1, text = "Electricity (in kWh):", padx = 50, pady =30)
elec_entry = ttk.Entry(tab1)

elec_label.grid(row=0, column=0)
elec_entry.grid(row = 0, column=1)

transport_button = ttk.Button(tab1, text = "Next: Transport", command = selec)
transport_button.grid(row = 1, column = 1)

bus_label = tk.Label(tab2, text = "Bus (in km):", padx = 50, pady =10)
bus_entry = ttk.Entry(tab2)

bus_label.grid(row=0, column=0)
bus_entry.grid(row = 0, column=1)

local_train_label = tk.Label(tab2, text = "Local Train (in km):", padx = 50, pady =10)
local_train_entry = ttk.Entry(tab2)

local_train_label.grid(row=1, column=0)
local_train_entry.grid(row = 1, column=1)

train_label = tk.Label(tab2, text = "Train (in km):", padx = 50, pady =10)
train_entry = ttk.Entry(tab2)

train_label.grid(row=2, column=0)
train_entry.grid(row = 2, column=1)

final_button = ttk.Button(root, text = "Calculate CFC", command = button_pressed)
final_button.pack(pady = 10)

final_text = tk.StringVar()
final_text.set("Calculate Carbon Footprint")
final_message = tk.Label(root, textvariable = final_text)
final_message.pack(pady = 10)

root.mainloop()
