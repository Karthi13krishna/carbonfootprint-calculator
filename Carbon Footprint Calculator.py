import tkinter as tk
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

a = [0,0,0,0]
b = ['Electricity','Bus','Local Train','Train']

def button_pressed():
    a[0] = calc(elec_entry.get(), 0.708, people_entry.get())
    a[1] = calc(bus_entry.get(),0.10312,1)
    a[2] = calc(local_train_entry.get(),0.036939994,1)
    a[3] = calc(train_entry.get(),0.00497,1)
    final_text.set("{:.2f}".format(sum(a)/1000) + " metric tons of CO2")
    
    y_label = tk.Label(result, text = "kg of CO2", padx = 10, pady =10)
    y_label.grid(row = 2, column = 0)
    
    f = Figure(figsize=(4,3), dpi=100)
    f.add_subplot(111).bar(b,a)
    result_bar = FigureCanvasTkAgg(f, result)
    result_bar.get_tk_widget().grid(row = 2, column = 1, padx = 10, pady = 10)
    
    maxi = b[a.index(max(a))]
    result_text.set("Your " + maxi + " emission is too high!. Try to reduce it :)")
    tabControl.select(3)
        
def selec0():
    tabControl.select(0)
def selec1():
    tabControl.select(1)
def selec2():
    tabControl.select(2)
def selec3():
    tabControl.select(3)   
    
def calc(var, val, people):
    try:
        carbon = (float(var) * val) / int(people)
    except:
        carbon = 0
    return carbon

root = tk.Tk()
style = ThemedStyle(root)
style.set_theme("plastik")
root.title("CarbonFootprint Calculator")
root.geometry("640x530")

tabControl = ttk.Notebook(root)
house = ttk.Frame(tabControl) 
transport = ttk.Frame(tabControl)
result = ttk.Frame(tabControl)
welcome = ttk.Frame(tabControl)

tabControl.add(welcome, text ='Welcome') 
tabControl.add(house, text ='House') 
tabControl.add(transport, text ='Transport')
tabControl.add(result, text = 'Result')
style.configure("Tab", focuscolor=style.configure(".")["background"])
tabControl.pack(expand = 1, fill ="both")

welcome_message = tk.Message(welcome, text = '''A carbon footprint is the measure of total greenhouse gas emissions, caused 
by an individual or an organization, expressed as carbon dioxide equivalent.
These greenhouse gases are released by our day-to-day activities including, 
but not limited to, transportation, electricity usage, the dress we wear and even 
the food we eat. We are taking buried carbon in the form of fossil fuels and 
releasing it to the atmosphere again. An increase in greenhouse gas 
emissions is the main cause for climate change. Many people are ignorant of 
this and keep adding more carbon to the atmosphere. To limit temperature rise
to 1.5°C, we must reduce our greenhouse gas emissions 7.6% each year for 
the next decade. Each individual must know how much carbon footprint they leave and know 
how much their activity affect the environment, so that they can be aware of 
their actions. In this project an easy-to-use carbon footprint calculator is 
developed. It can be used by anyone to calculate how much carbon they emit. 
It also provides smart suggestions based on their carbon emission and help 
them reduce their carbon footprint. Moving forward in technology is good, but 
we also want to start taking care of our environment, smartly''').pack(padx = 10, pady = 10)
house1_button = ttk.Button(welcome, text = "Next: House", command = selec1).pack(padx = 100, pady = 10)

people_label = tk.Label(house, text = "No of persons in the house:", padx = 50, pady =10).grid(row=0, column=0)
people_entry = ttk.Entry(house)
people_entry.grid(row = 0, column=1)

elec_label = tk.Label(house, text = "Electricity (in kWh):", padx = 50, pady =10).grid(row=1, column=0)
elec_entry = ttk.Entry(house)
elec_entry.grid(row = 1, column=1)

welcome_button = ttk.Button(house, text = "Back: Welcome", command = selec0).grid(row = 2, column = 0, pady = 10)
transport_button = ttk.Button(house, text = "Next: Transport", command = selec2).grid(row = 2, column = 1, pady = 10)

bus_label = tk.Label(transport, text = "Bus (in km):", padx = 50, pady =10).grid(row=0, column=0)
bus_entry = ttk.Entry(transport)
bus_entry.grid(row = 0, column=1)

local_train_label = tk.Label(transport, text = "Local Train (in km):", padx = 50, pady =10).grid(row=1, column=0)
local_train_entry = ttk.Entry(transport)
local_train_entry.grid(row = 1, column=1)

train_label = tk.Label(transport, text = "Train (in km):", padx = 50, pady =10).grid(row=2, column=0)
train_entry = ttk.Entry(transport)
train_entry.grid(row = 2, column=1)

house_button = ttk.Button(transport, text = "Back: House", command = selec1).grid(row = 3, column = 0, pady = 10)
result_button = ttk.Button(transport, text = "Next: Result", command = selec3).grid(row = 3, column = 1, pady = 10)

result_text = tk.StringVar()
result_text.set("Enter the values to calculate your Carbon footprint")
result_message = tk.Label(result, textvariable = result_text).grid(row = 1, column = 1, padx = 50, pady = 10)

final_text = tk.StringVar()
final_text.set("Calculate Carbon Footprint")
final_message = tk.Label(result, textvariable = final_text).grid(row = 0, column = 1, padx = 50, pady = 10)

transport1_button = ttk.Button(result, text = "Back: Transport", command = selec2).grid(row = 3, column = 0, padx = 10,pady = 10)

final_button = ttk.Button(root, text = "Calculate CarbonFootprint", command = button_pressed).pack(pady = 20)

root.mainloop()
