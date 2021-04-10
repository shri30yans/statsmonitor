import psutil,GPUtil,cpuinfo
import time,serial,sys,json,os
from tkinter import * #pylint:disable=unused-wildcard-import
import tkinter.ttk as ttk
from tkinter import messagebox
from threading import Thread
import serial.tools.list_ports


# Import cpuinfo.py from up one directory
sys.path.append('../cpuinfo')

run = False # Default value of run is False
ser_port=None #Serial port where Arduino is connected

# --- GUI functions ---

#function called when the GUI switch is pressed    
def switch():
    global run   
    if ser_port == None:
        myButton.config(image = myButton_off)#change button image to on
        statusLabel.config(text = "Choose a serial device from the drop down to run the program.", fg = "grey")#Change the Label
        run = False #pause program

    elif run:
        myButton.config(image = myButton_off)#change button image to off
        statusLabel.config(text = "Program is paused. Click on the button to resume.", fg = "grey")#Change the Label
        run = False #pause program
    else:
        myButton.config(image = myButton_on)#change button image to on
        statusLabel.config(text = "Program is running. Click on the button to pause.", fg = "green")#Change the Label
        run = True #resume program

    





def serial_ports():    
    #list of all serial port devices connected to our computer
    return serial.tools.list_ports.comports()

   

def update_ports():
    #update the dropdown with the list of all serial port devices connected to our computer
    #called each time after the Dropdown is clicked
    ports = list(serial.tools.list_ports.comports()) 
    cb["values"] =ports

#when new option is selected from the dropdown
def on_select(event=None):
    global ser_port,arduino
    #get selection from combobox
    ser_port =  cb.get()
    port_number=str(ser_port).split()[0]
    arduino = serial.Serial(port=port_number, baudrate=115200, timeout=.1)

#when the X is pressed
def on_closing():
    #More options: https://www.geeksforgeeks.org/python-tkinter-messagebox-widget/#:~:text=Python%20Tkinter%20%E2%80%93%20MessageBox%20Widget%20is,provides%20a%20number%20of%20functions.
    if messagebox.askokcancel("Quit", "Do you want to quit? This will exit your program."):
        root.withdraw()
        #root.destroy()



# --- Stats functions ---

#sending to Arduino using Serial
def write_read(x):
    global ser_port, arduino,run
    if ser_port != None and run == True:
        try:
            arduino.write(bytes(x, 'utf-8'))
            connectionLabel.config(text ="")
            #uncomment this line if you want to print the data sent to Arduino
            #print(f"Sent {x} to Arduino")
            #uncomment these line if you want to see the Data sent by the arduino
            #data = arduino.read(arduino.inWaiting()).decode("utf-8") 
            #return data
        except serial.serialutil.SerialException:
            ser_port=None 
            switch()#change switch to off
            cb.set('')#empty the combobox
            #show user the error in connectionLabel
            connectionLabel.config(text = f"Arduino is not detected. Reconnect or choose a different serial device.", fg = "red")
            time.sleep(2)


#collecting data from user
def collect_data():
    gpus = GPUtil.getGPUs()
    gpu=gpus[0]
    while True:
        if ser_port !=None:
            stats_dictionary={}
            if run:#if button is set to True
                stats_dictionary["CPU_name"]=cpuinfo.get_cpu_info()["brand_raw"].split("@")[0].split(" ")[2]
                stats_dictionary["CPU_load"]=f"{psutil.cpu_percent()}%"   
                stats_dictionary["RAM_percentage"]=f"{psutil.virtual_memory().percent}%"

                stats_dictionary["GPU_name"]=gpu.name
                stats_dictionary["GPU_load"]=f"{gpu.load*100}%"
                #stats_dictionary["GPU_free_memory"]=f"{gpu.memoryFree}MB"   # get free memory in MB format
                #stats_dictionary["GPU_used_memory"]=f"{gpu.memoryUsed}MB"   # get used memory
                #stats_dictionary["GPU_gpu_total_memory"]=f"{gpu.memoryTotal}MB" # get total memory
                stats_dictionary["GPU_temp"]=f"{gpu.temperature} °C"    # get GPU temperature in Celsius

                stats_dictionary_json=json.dumps(stats_dictionary)#covert to json
                write_read(f"{stats_dictionary_json}")#send json file
                #print(stats_dictionary)
                #print("Returned data",value)
            else:
                while run == False:
                    time.sleep(3)


#function to ruk collect_data() in another thread
def start_collect_data():
    t = Thread (target = collect_data)
    t.start()

# --- GUI Main ---

root = Tk() # Create Object
# Add Title
root.title('Stats Monitor')
 # Adding Geometry
root.geometry("500x300")

#set images of button
myButton_on = PhotoImage(file = "Images/on.png")
myButton_off = PhotoImage(file = "Images/off.png")

#Create Button object
myButton = Button(root, image = myButton_off, bd = 0,command = switch)
myButton.pack(pady = 50)

#Default statusLabel
statusLabel = Label(root,text = "Choose a serial device from the drop down to run the program.", fg = "grey")
statusLabel.pack(pady = 20)

#create Combobox object
cb = ttk.Combobox(root, values=serial_ports(), width=32,postcommand=update_ports)
cb.pack()

# assign function to combobox
cb.bind('<<ComboboxSelected>>', on_select)

#default value of connectionLabel
connectionLabel = Label(root,text = " ")
connectionLabel.pack(pady = 20)

#to specify the protocol to follow when window is closed ie X is pressed
root.protocol("WM_DELETE_WINDOW", on_closing)


root.after(1,start_collect_data)  # After 1ms second, call start_collect_data which will run collect_data in another thread
root.mainloop()




        
    








