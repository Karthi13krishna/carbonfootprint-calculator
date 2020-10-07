from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import csv
from geopy.distance import distance
from PIL import ImageTk

# Global Variables
a = [0,0,0,0]
average = [1100,700,800,1800]
b = ['Energy','Food','Transportation', 'Flights']
iata_codes = []
dist = 0.0
dist1 = 0.0
lpg_option = 14.2

# Reading values from airport database
with open('airport_codes.csv', mode = 'r') as airport_codes:
    csvreader = csv.reader(airport_codes)
    for i in csvreader:
        iata_codes.append(i[2])

# Getting the airport's coordinates
def flight_coordinates(iata):
    with open('airport_codes.csv', mode = 'r') as airport_codes:
        csvreader = csv.reader(airport_codes)
        for i in csvreader:
            if iata in i[2]:
                x,y = (i[3]).split(",")
                break
        return float(x),float(y)

# Calculating flight distance        
def flight_distance(iata1, iata2):
    try:
        d1 = flight_coordinates(iata1)
        d2 = flight_coordinates(iata2)
    except:
        d1 = 0.0,0.0
        d2 = 0.0,0.0
    return distance(d1,d2).km

# Getting value from the flight combobox
def flight_func(event):
    try:
        src_option, dest_option = src_combo.get(), dest_combo.get()
        src_option1, dest_option1 = src_combo2.get(), dest_combo2.get()
    except:
        src_option, dest_option = 0,0
        src_option1, dest_option1 = 0,0
    global dist, dist1 
    dist = round(flight_distance(src_option, dest_option),2)
    dist1 = round(flight_distance(src_option1, dest_option1),2)

# Getting value from LPG Combobox
def lpg_func(event):
    lpg = lpg_combo.get()
    global lpg_option
    lpg_option = float(lpg)*1.55537*1.8

# Calculations to be done when the calculate button is pressed
def button_pressed():
    try:
        x = float(trip_var.get())*int(trip_spin.get())*int(passenger_spin.get())
    except:
        x = 1
    try:
        y = float(trip_var2.get())*int(trip_spin2.get())*int(passenger_spin2.get())
    except:
        y = 1
    
    duration = (duration_value[duration_list.index(duration_choice.get())])/365
    avg = [round(i * duration, 2) for i in average]
    
    a[0] = (calc(elec_entry.get(), 0.708, people_entry.get()) 
            + calc(lpg_spin.get(), lpg_option, people_entry.get()))
    
    a[1] = (calc(beef_entry.get(), 27, people_entry.get())
            + calc(cheese_entry.get(), 13.5/1000, people_entry.get())
            + calc(chicken_entry.get(), 6.9, people_entry.get())
            + calc(fish_entry.get(), 6.1, people_entry.get()))
    
    a[2] = (calc(bus_entry.get(),0.10312,1) 
            + calc(local_train_entry.get(),0.036939994,1) 
            + calc(train_entry.get(),0.00497,1) 
            + calc(dist1_entry.get(),veh1_var.get(),mile1_entry.get()) 
            + calc(dist2_entry.get(),veh2_var.get(),mile2_entry.get()))
    flight_value = class_value[class_name.index(class_choice.get())]
    flight_value1 = class_value[class_name.index(class_choice2.get())]
    
    a[3] = calc(dist, 0.158*1.891*flight_value*x, 1) + calc(dist1, 0.158*1.891*flight_value1*y, 1)
    final_text.set("{:.2f}".format(sum(a)/1000) + " metric tons of CO2")
    
    result_button = Button(flight, text = "Next: Result", command = selec4).place(relx = 0.7, rely = 0.9, anchor = 'w')    
    flight_button = Button(result, text = "Back: Flight", command = selec3).place(relx = 0.3, rely = 0.9, anchor = 'e')
    Suggestion_button = Button(result, text = "Next: Suggestions", command = selec5).place(relx = 0.7, rely = 0.9, anchor = 'w')
    result1_button = Button(suggestion, text = "Back: Result", command = selec4).place(relx = 0.3, rely = 0.9, anchor = 'e')
    
    
    f = Figure(figsize=(7,4), dpi=100)
    f.patch.set_facecolor('#2D2D2D')
    graph = f.add_subplot(111)
    x = np.arange(len(b))
    width = 0.35
    rects1 = graph.bar(x - width/2, a, width, label='Your carbon footprint')
    rects2 = graph.bar(x + width/2, avg, width, label='Average carbon footprint')
    graph.spines["bottom"].set_color("white")
    graph.spines["left"].set_color("white")
    graph.spines["top"].set_color("#2D2D2D")
    graph.spines["right"].set_color("#2D2D2D")
    graph.set_facecolor('#2D2D2D')
    graph.set_xticks(x)
    graph.set_xticklabels(b)
    graph.tick_params(axis='x', colors='white')
    graph.tick_params(axis='y', colors='white')
    graph.set_ylabel('kg of CO2', color = 'white')
    graph.legend()
    
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            graph.annotate('{:.2f}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', color='white')
    autolabel(rects1)
    autolabel(rects2)
    
    result_bar = FigureCanvasTkAgg(f, result)
    result_bar.get_tk_widget().place(relx = 0.5, rely = 0.5, anchor = 'center')
    result_bar.draw()
    
    toolbar = NavigationToolbar2Tk(result_bar, result)
    toolbar.update()
    toolbar.config(background='#2D2D2D')
    result_bar.get_tk_widget().place(relx = 0.5, rely = 0.5, anchor = 'center')
     
    maxi = b[a.index(max(a))]
    result_text.set("Your " + maxi + " emission is too high!. Try to reduce it :)")
    tabControl.select(4)
    tabControl.add(suggestion, text = 'Suggestions')

    
# Functions for switching tabs 
def selec0():
    tabControl.select(0)
def selec1():
    tabControl.select(1)
def selec2():
    tabControl.select(2)
def selec3():
    tabControl.select(3)   
def selec4():
    tabControl.select(4)
def selec5():
    tabControl.select(5)

# Function for backend calculation  
def calc(var, val, people):
    try:
        carbon = (float(var) * float(val)) / float(people)
    except:
        carbon = 0
    return round(carbon,2)

# Graphical user inferface
root = tk.Tk()
style = ThemedStyle(root)
style.set_theme("plastik")
style.configure('TButton', background = '#C5D961', foreground = '#2D2D2D', focusthickness=3, focuscolor='none')
style.map('TButton', background=[('active','#C5D961')])
root.title("CarbonFootprint Calculator")
root.iconbitmap('D:/Carbon footprint calculator/logo.ico')
root.geometry("700x600")
root['bg'] = '#2D2D2D'

# Creating tabs
tabControl = ttk.Notebook(root)
welcome = Frame(tabControl, bg = '#2D2D2D')
house = Frame(tabControl, bg = '#2D2D2D') 
transport = Frame(tabControl, bg = '#2D2D2D')
flight = Frame(tabControl, bg = '#2D2D2D')
result = Frame(tabControl, bg = '#2D2D2D')
suggestion = Frame(tabControl, bg = '#2D2D2D')

# Adding tabs
tabControl.add(welcome, text ='Welcome') 
tabControl.add(house, text ='House') 
tabControl.add(transport, text ='Transport')
tabControl.add(flight, text ='Flight')
tabControl.add(result, text = 'Result')

tabControl.hide(result)
style.configure("Tab", focuscolor=style.configure(".")["background"])
tabControl.pack(expand = 1, fill ="both")

# Welcome tab (1st tab)
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
we also want to start taking care of our environment, smartly''', bg = '#2D2D2D', fg = 'white').pack(padx = 10, pady = 10)

duration_label = tk.Label(welcome, text = 'Enter the period this calculation covers:', padx = 20, pady =10, bg = '#2D2D2D', fg = 'white').place(relx = 0.1, rely = 0.78, anchor = 'w')
duration_choice = StringVar(welcome)
duration_list = ['1 Week', '1 Month', '1 Year']
duration_value = [7,30,365]
duration_option = OptionMenu(welcome, duration_choice, *duration_list)
duration_option.config(bg = '#2D2D2D',fg = 'white', activebackground = '#2D2D2D', activeforeground = 'white')
duration_option['menu'].config(bg = '#2D2D2D',fg = 'white', activeforeground = '#2D2D2D', activebackground = 'white')
duration_choice.set(duration_list[2])
duration_option.place(relx = 0.6, rely = 0.75)


house1_button = Button(welcome, text = "Next: House", command = selec1).place(relx = 0.7, rely = 0.9, anchor = 'w')

# House tab (2nd tab)
house1 = LabelFrame(house, text="Energy", bg = '#2D2D2D', fg = 'white', padx = 10, pady =5)  
house1.pack(fill="both", expand="yes")

people_label = tk.Label(house1, text = "No of persons in the house:", padx = 20, pady =10, bg = '#2D2D2D', fg = 'white').grid(row=0, column=0)
people_entry = tk.Spinbox(house1,from_ = 1, to = 10, width = 8)
people_entry.grid(row = 0, column=1)

elec_label = tk.Label(house1, text = "Electricity (in kWh):", padx = 20, pady =10, bg = '#2D2D2D', fg = 'white').grid(row=1, column=0)
elec_entry = Entry(house1, width = 10)
elec_entry.grid(row = 1, column=1)

lpg_label = tk.Label(house1, text = "Number of LPG cylinders used:", padx = 20, pady =10, bg = '#2D2D2D', fg = 'white').grid(row=2, column=0)
lpg_spin = ttk.Spinbox(house1,from_ = 1, to = 10, width = 8)
lpg_spin.grid(row = 2, column=1)
lpg_combo = ttk.Combobox(house1, value= [14.2,5,19,47.5], width = 8)
lpg_combo.bind("<<ComboboxSelected>>", lpg_func)
lpg_combo.set(14.2)
lpg_combo.grid(row = 2, column = 2, padx = 10)

house2 = LabelFrame(house, text="Food", bg = '#2D2D2D', fg = 'white', padx = 10, pady =5)  
house2.pack(fill="both", expand="yes")

beef_label = tk.Label(house2, text = "Beef (in kg):", padx = 20, pady =10, bg = '#2D2D2D', fg = 'white').grid(row=0, column=0)
beef_entry = Entry(house2, width = 10)
beef_entry.grid(row = 0, column=1)

cheese_label = tk.Label(house2, text = "Cheese (in g):", padx = 20, pady =10, bg = '#2D2D2D', fg = 'white').grid(row=1, column=0)
cheese_entry = Entry(house2, width = 10)
cheese_entry.grid(row = 1, column=1)

chicken_label = tk.Label(house2, text = "Chicken (in kg):", padx = 20, pady =10, bg = '#2D2D2D', fg = 'white').grid(row=2, column=0)
chicken_entry = Entry(house2, width = 10)
chicken_entry.grid(row = 2, column=1)

fish_label = tk.Label(house2, text = "fish (in kg):", padx = 20, pady =10, bg = '#2D2D2D', fg = 'white').grid(row=3, column=0)
fish_entry = Entry(house2, width = 10)
fish_entry.grid(row = 3, column=1)

welcome_button = Button(house, text = "Back: Welcome", command = selec0).place(relx = 0.3, rely = 0.9, anchor = 'e')
final_button = Button(house, text = "Calculate Carbon Footprint", command = button_pressed).place(relx = 0.5, rely = 0.9, anchor = 'center')
transport_button = Button(house, text = "Next: Transport", command = selec2).place(relx = 0.7, rely = 0.9, anchor = 'w')

# Transport tab (3rd tab)
labelframe1 = LabelFrame(transport, text="Personal Vehicle", bg = '#2D2D2D', fg = 'white', padx = 10, pady =5)  
labelframe1.pack(fill="both", expand="yes") 

mile1_label = tk.Label(labelframe1, text = "Milage (vehicle 1)", padx = 20, pady =10, bg = '#2D2D2D', fg = 'white').grid(row=0, column=0)
mile1_entry = Entry(labelframe1, width = 10)
mile1_entry.grid(row = 0, column=1)

veh1_var = DoubleVar()
veh1_var.set(2.68)
veh1_R1 = Radiobutton(labelframe1, text="Diesel",variable = veh1_var, value=2.68, bg = '#2D2D2D', fg = 'white', activebackground = '#2D2D2D',activeforeground= 'white',selectcolor = '#2D2D2D')
veh1_R1.grid(row = 0, column = 2, padx = 10)
veh1_R2 = Radiobutton(labelframe1, text="Petrol",variable = veh1_var, value=2.31, bg = '#2D2D2D', fg = 'white', activebackground = '#2D2D2D',activeforeground= 'white',selectcolor = '#2D2D2D')
veh1_R2.grid(row = 0, column = 3, padx = 10)

dist1_label = tk.Label(labelframe1, text = "Distance (vehicle 1)", padx = 20, pady =10, bg = '#2D2D2D', fg = 'white').grid(row=1, column=0)
dist1_entry = Entry(labelframe1, width = 10)
dist1_entry.grid(row = 1, column=1)

mile2_label = tk.Label(labelframe1, text = "Milage (vehicle 2)", padx = 20, pady =10, bg = '#2D2D2D', fg = 'white').grid(row=2, column=0)
mile2_entry = Entry(labelframe1, width = 10)
mile2_entry.grid(row = 2, column=1)

veh2_var = DoubleVar()
veh2_var.set(2.68)
veh2_R1 = Radiobutton(labelframe1, text="Diesel",variable = veh2_var, value=2.68, bg = '#2D2D2D', fg = 'white', activebackground = '#2D2D2D',activeforeground= 'white',selectcolor = '#2D2D2D')
veh2_R1.grid(row = 2, column = 2, padx = 10)
veh2_R2 = Radiobutton(labelframe1, text="Petrol",variable = veh2_var, value=2.31, bg = '#2D2D2D', fg = 'white', activebackground = '#2D2D2D',activeforeground= 'white',selectcolor = '#2D2D2D')
veh2_R2.grid(row = 2, column = 3, padx = 10)

dist2_label = tk.Label(labelframe1, text = "Distance (vehicle 2)", padx = 20, pady =10, bg = '#2D2D2D', fg = 'white').grid(row=3, column=0)
dist2_entry = Entry(labelframe1, width = 10)
dist2_entry.grid(row = 3, column=1)

labelframe2 = LabelFrame(transport, text="Public transport", bg = '#2D2D2D', fg = 'white', padx = 10, pady =5)  
labelframe2.pack(fill="both", expand="yes")

bus_label = tk.Label(labelframe2, text = "Bus (in km):", padx = 20, pady =10, bg = '#2D2D2D', fg = 'white').grid(row=0, column=0)
bus_entry = Entry(labelframe2, width = 10)
bus_entry.grid(row = 0, column=1)

local_train_label = tk.Label(labelframe2, text = "Local Train (in km):", padx = 20, pady =10, bg = '#2D2D2D', fg = 'white').grid(row=1, column=0)
local_train_entry = Entry(labelframe2, width = 10)
local_train_entry.grid(row = 1, column=1)

train_label = tk.Label(labelframe2, text = "Train (in km):", padx = 20, pady =10, bg = '#2D2D2D', fg = 'white').grid(row=2, column=0)
train_entry = Entry(labelframe2, width = 10)
train_entry.grid(row = 2, column=1)

house_button = Button(transport, text = "Back: House", command = selec1).place(relx = 0.3, rely = 0.9, anchor = 'e')
final_button = Button(transport, text = "Calculate Carbon Footprint", command = button_pressed).place(relx = 0.5, rely = 0.9, anchor = 'center')
flight_button = Button(transport, text = "Next: Flight", command = selec3).place(relx = 0.7, rely = 0.9, anchor = 'w')

# Flight tab (4th Tab)
flight1 = LabelFrame(flight, text="Trip 1", bg = '#2D2D2D', fg = 'white', padx = 10, pady =5)  
flight1.pack(fill="both")

src_label = tk.Label(flight1, text = "Source (IATA Code):", padx = 20, pady =10, bg = '#2D2D2D', fg = 'white').grid(row=0, column=0)
src_combo = ttk.Combobox(flight1, value = iata_codes[1:] , width = 10)
src_combo.bind("<<ComboboxSelected>>", flight_func)
src_combo.grid(row = 0, column = 1, padx = 10, pady = 10)

dest_label = tk.Label(flight1, text = "Destination (IATA Code):", padx = 20, pady =10, bg = '#2D2D2D', fg = 'white').grid(row=1, column=0)
dest_combo = ttk.Combobox(flight1, value = iata_codes[1:] , width = 10)
dest_combo.bind("<<ComboboxSelected>>", flight_func)
dest_combo.grid(row = 1, column = 1, padx = 10, pady = 10)

class_choice = StringVar(flight1)
class_label = tk.Label(flight1, text = "Class:", padx = 20, pady =10, bg = '#2D2D2D', fg = 'white').grid(row=2, column=0)
class_name = ['Economy', 'Business', 'First Class']
class_value = [1,2.37,3]
flight_class = OptionMenu(flight1, class_choice, *class_name)
flight_class.config(bg = '#2D2D2D',fg = 'white', activebackground = '#2D2D2D', activeforeground = 'white')
flight_class['menu'].config(bg = '#2D2D2D',fg = 'white', activeforeground = '#2D2D2D', activebackground = 'white')
class_choice.set(class_name[0])
flight_class.grid(row = 2, column = 1, padx = 10, pady = 10)

trip_var = DoubleVar()
trip_var.set(1)
return_trip = Radiobutton(flight1, text="Return trip",variable = trip_var, value=1, bg = '#2D2D2D', fg = 'white', activebackground = '#2D2D2D',activeforeground= 'white',selectcolor = '#2D2D2D')
return_trip.grid(row = 2, column = 2, padx = 10)
one_way_trip = Radiobutton(flight1, text="One Way trip",variable = trip_var, value=0.5, bg = '#2D2D2D', fg = 'white', activebackground = '#2D2D2D',activeforeground= 'white',selectcolor = '#2D2D2D')
one_way_trip.grid(row = 2, column = 3, padx = 10)

passenger_label = tk.Label(flight1, text = "Number of Passengers:", padx = 20, pady =10, bg = '#2D2D2D', fg = 'white').grid(row=3, column=0)
passenger_spin = ttk.Spinbox(flight1,from_ = 1, to = 10, width = 10)
passenger_spin.grid(row = 3, column=1)

trip_label = tk.Label(flight1, text = "Number of trips", padx = 20, pady =10, bg = '#2D2D2D', fg = 'white').grid(row=3, column=2)
trip_spin = ttk.Spinbox(flight1,from_ = 1, to = 10, width = 10)
trip_spin.grid(row = 3, column=3)


flight2 = LabelFrame(flight, text="Trip 2", bg = '#2D2D2D', fg = 'white', padx = 10, pady =5)  
flight2.pack(fill="both", expand='yes')

src_label2 = tk.Label(flight2, text = "Source (IATA Code):", padx = 20, pady =10, bg = '#2D2D2D', fg = 'white').grid(row=0, column=0)
src_combo2 = ttk.Combobox(flight2, value = iata_codes[1:] , width = 10)
src_combo2.bind("<<ComboboxSelected>>", flight_func)
src_combo2.grid(row = 0, column = 1, padx = 10, pady = 10)

dest_label2 = tk.Label(flight2, text = "Destination (IATA Code):", padx = 20, pady =10, bg = '#2D2D2D', fg = 'white').grid(row=1, column=0)
dest_combo2 = ttk.Combobox(flight2, value = iata_codes[1:] , width = 10)
dest_combo2.bind("<<ComboboxSelected>>", flight_func)
dest_combo2.grid(row = 1, column = 1, padx = 10, pady = 10)

class_choice2 = StringVar(flight2)
class_label2 = tk.Label(flight2, text = "Class:", padx = 20, pady =10, bg = '#2D2D2D', fg = 'white').grid(row=2, column=0)
flight_class2 = OptionMenu(flight2, class_choice2, *class_name)
flight_class2.config(bg = '#2D2D2D',fg = 'white', activebackground = '#2D2D2D', activeforeground = 'white')
flight_class2['menu'].config(bg = '#2D2D2D',fg = 'white', activeforeground = '#2D2D2D', activebackground = 'white')
class_choice2.set(class_name[0])
flight_class2.grid(row = 2, column = 1, padx = 10, pady = 10)

trip_var2 = DoubleVar()
trip_var2.set(1)
return_trip2 = Radiobutton(flight2, text="Return trip",variable = trip_var2, value=1, bg = '#2D2D2D', fg = 'white', activebackground = '#2D2D2D',activeforeground= 'white',selectcolor = '#2D2D2D')
return_trip2.grid(row = 2, column = 2, padx = 10)
one_way_trip2 = Radiobutton(flight2, text="One Way trip",variable = trip_var2, value=0.5, bg = '#2D2D2D', fg = 'white', activebackground = '#2D2D2D',activeforeground= 'white',selectcolor = '#2D2D2D')
one_way_trip2.grid(row = 2, column = 3, padx = 10)

passenger_label2 = tk.Label(flight2, text = "Number of Passengers:", padx = 20, pady =10, bg = '#2D2D2D', fg = 'white').grid(row=3, column=0)
passenger_spin2 = ttk.Spinbox(flight2,from_ = 1, to = 10, width = 10)
passenger_spin2.grid(row = 3, column=1)

trip_label2 = tk.Label(flight2, text = "Number of trips", padx = 20, pady =10, bg = '#2D2D2D', fg = 'white').grid(row=3, column=2)
trip_spin2 = ttk.Spinbox(flight2,from_ = 1, to = 10, width = 10)
trip_spin2.grid(row = 3, column=3)

transport_button_button = Button(flight, text = "Back: Transport", command = selec2).place(relx = 0.3, rely = 0.9, anchor = 'e')
final_button = Button(flight, text = "Calculate Carbon Footprint", command = button_pressed).place(relx = 0.5, rely = 0.9, anchor = 'center')

# Result tab (5th tab)
result_text = tk.StringVar()
result_text.set("Enter the values to calculate your Carbon footprint")
final_text = tk.StringVar()
final_text.set("Calculate Carbon Footprint")

result_message = tk.Label(result, textvariable = result_text, bg = '#2D2D2D', fg = 'white').place(relx = 0.5, rely = 0.05, anchor = 'center')
final_message = tk.Label(result, textvariable = final_text, bg = '#2D2D2D', fg = 'white').place(relx = 0.5, rely = 0.1, anchor = 'center')



# Suggestion tab (6th tab)
'''suggestion_text = tk.StringVar()
suggestion_text.set("Calculate Carbon Footprint")
suggestion_message = tk.Text(suggestion, textvariable = suggestion_text, bg = '#2D2D2D', fg = 'white').place(relx = 0.5, rely = 0.05, anchor = 'center')'''

root.mainloop()
