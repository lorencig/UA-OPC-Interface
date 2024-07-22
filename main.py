import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from opcua import Client, ua
import threading
import time
import ttkbootstrap as ttk
from ttkbootstrap import Style

# Default OPC UA client connection
client = Client("opc.tcp://localhost:4840/")
client.connect()

# Define default pump nodes
pumpA = client.get_node("ns=1;i=1001")
pumpB = client.get_node("ns=1;i=1002")

# Define default method nodes
pump = client.get_node("ns=2;i=2001")
stop = client.get_node("ns=2;i=2002")
empty = client.get_node("ns=2;i=2003")
fill = client.get_node("ns=2;i=2004")

# Event to control the execution flow
stop_event = threading.Event()

# List to store the user-created program
program = []

# Start time of the process
start_time = None

# Function to add actions to the program
def add_action(action, pump_node):
    if action in ["Pump", "Fill", "Empty"]:
        value = simpledialog.askinteger("Input", f"Enter value for {action} (1-1000 μL/min):", minvalue=1, maxvalue=1000)
        if value is not None:
            program.append((action, pump_node, value))
        else:
            messagebox.showerror("Error", "Value is required")
    elif action == "Stop":
        program.append((action, pump_node, 0))
    update_program_table()

def add_time_interval():
    time_interval = simpledialog.askinteger("Input", "Enter time interval (seconds):", minvalue=1, maxvalue=36000)
    if time_interval is not None:
        program.append(("Sleep", None, time_interval))
        update_program_table()
    else:
        messagebox.showerror("Error", "Time interval is required")

def update_program_table():
    for row in program_table.get_children():
        program_table.delete(row)
    for index, (action, pump_node, value) in enumerate(program):
        pump_name = "A" if pump_node == pumpA else "B" if pump_node == pumpB else ""
        program_table.insert("", "end", iid=index, values=(index+1, action, pump_name, value))

def clear_program():
    global program
    program = []
    update_program_table()

def execute_program():
    global start_time
    stop_event.set()
    threading.Thread(target=run_program).start()

def update_timer():
    while not stop_event.is_set():
        elapsed_time = time.time() - start_time
        timer_label.config(text=f"Elapsed Time: {int(elapsed_time)}s")
        time.sleep(1)

def run_program():
    global start_time
    stop_event.clear()
    status_label.config(text="Executing program...")
    for action, pump_node, value in program:
        if stop_event.is_set():
            break
        start_time = time.time()  # Restart timer for each action
        threading.Thread(target=update_timer).start()
        if action == "Sleep":
            for _ in range(value):
                if stop_event.is_set():
                    break
                time.sleep(1)
        else:
            method_node = eval(action.lower())
            pump_name = "Pump A" if pump_node == pumpA else "Pump B" if pump_node == pumpB else ""
            try:
                status_label.config(text=f"Executing: {action} on {pump_name} with value {value}")
                if action == "Stop":
                    pump_node.call_method(stop)
                else:
                    input_arg = [ua.Variant(value, ua.VariantType.UInt16)]
                    pump_node.call_method(method_node, *input_arg)
            except Exception as e:
                status_label.config(text=f"Error: {e}")
                break
    status_label.config(text="Program finished")
    
# Create the main window
root = tk.Tk()
root.title("UA OPC Interface")
icon = tk.PhotoImage(file="brain.png")
root.iconphoto(True, icon)

# Create status label
status_label = tk.Label(root, text="Idle", fg="blue")
status_label.grid(row=0, column=0, columnspan=4, pady=(10, 10), sticky="ew")

# Create timer label
timer_label = tk.Label(root, text="Elapsed Time: 0s", fg="blue")
timer_label.grid(row=0, column=4, pady=(10, 10), sticky="ew")

# Create program table
program_table = ttk.Treeview(root, columns=("Step", "Action", "Pump", "Value"), show="headings")
program_table.heading("Step", text="Step")
program_table.heading("Action", text="Action")
program_table.heading("Pump", text="Pump")
program_table.heading("Value", text="Value")
program_table.column("Step", anchor="center")
program_table.column("Action", anchor="center")
program_table.column("Pump", anchor="center")
program_table.column("Value", anchor="center")
program_table.grid(row=1, column=0, columnspan=5, pady=(10, 10), sticky="nsew")

# Load button icons
pump_icon = tk.PhotoImage(file='pump.png')
pump_icon_resized = pump_icon.subsample(5, 5)

stop_icon = tk.PhotoImage(file='stop.png')
stop_icon_resized = stop_icon.subsample(5, 5)

clean_icon = tk.PhotoImage(file='clean.png')
clean_icon_resized = clean_icon.subsample(5, 5)

empty_icon = tk.PhotoImage(file='empty.png')
empty_icon_resized = empty_icon.subsample(5, 5)

fill_icon = tk.PhotoImage(file='fill.png')
fill_icon_resized = fill_icon.subsample(5, 5)

time_icon = tk.PhotoImage(file='time.png')
time_icon_resized = time_icon.subsample(5, 5)

submit_icon = tk.PhotoImage(file='submit.png')
submit_icon_resized = submit_icon.subsample(4, 4)

# Create frames for Pump A and Pump B
pumpA_frame = ttk.LabelFrame(root, text="Pump A", padding=(10, 10))
pumpA_frame.grid(row=2, column=0, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="nsew")

pumpB_frame = ttk.LabelFrame(root, text="Pump B", padding=(10, 10))
pumpB_frame.grid(row=2, column=4, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="nsew")

# Create buttons for Pump A
btn_pump_a = ttk.Button(pumpA_frame, text="Pump A", command=lambda: add_action("Pump", pumpA), image=pump_icon_resized, compound=tk.TOP)
btn_pump_a.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")

btn_stop_a = ttk.Button(pumpA_frame, text="Stop A", command=lambda: add_action("Stop", pumpA), image=stop_icon_resized, compound=tk.TOP)
btn_stop_a.grid(row=0, column=1, padx=(5, 5), pady=(5, 5), sticky="nsew")

btn_fill_a = ttk.Button(pumpA_frame, text="Fill A", command=lambda: add_action("Fill", pumpA), image=fill_icon_resized, compound=tk.TOP)
btn_fill_a.grid(row=1, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")

btn_empty_a = ttk.Button(pumpA_frame, text="Empty A", command=lambda: add_action("Empty", pumpA), image=empty_icon_resized, compound=tk.TOP)
btn_empty_a.grid(row=1, column=1, padx=(5, 5), pady=(5, 5), sticky="nsew")

# Create buttons for Pump B
btn_pump_b = ttk.Button(pumpB_frame, text="Pump B", command=lambda: add_action("Pump", pumpB), image=pump_icon_resized, compound=tk.TOP)
btn_pump_b.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")

btn_stop_b = ttk.Button(pumpB_frame, text="Stop B", command=lambda: add_action("Stop", pumpB), image=stop_icon_resized, compound=tk.TOP)
btn_stop_b.grid(row=0, column=1, padx=(5, 5), pady=(5, 5), sticky="nsew")

btn_fill_b = ttk.Button(pumpB_frame, text="Fill B", command=lambda: add_action("Fill", pumpB), image=fill_icon_resized, compound=tk.TOP)
btn_fill_b.grid(row=1, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")

btn_empty_b = ttk.Button(pumpB_frame, text="Empty B", command=lambda: add_action("Empty", pumpB), image=empty_icon_resized, compound=tk.TOP)
btn_empty_b.grid(row=1, column=1, padx=(5, 5), pady=(5, 5), sticky="nsew")

#Separator
separator = ttk.Separator(root, orient='vertical')
separator.grid(row=2, column=2, padx=75)
separator = ttk.Separator(root, orient='vertical')    
separator.grid(row=4, column=2, padx=75)

# Create additional buttons
btn_time_interval = ttk.Button(root, text="Time Interval", command=add_time_interval, image=time_icon_resized, compound=tk.TOP)
btn_time_interval.grid(row=4, column=0, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="nsew")

btn_submit = ttk.Button(root, text="Submit", command=execute_program, image=submit_icon_resized, compound=tk.TOP)
btn_submit.grid(row=5, column=0, columnspan=6, padx=(10, 10), pady=(10, 10), sticky="nsew")

btn_clear = ttk.Button(root, text="Clear", command=clear_program, image=clean_icon_resized, compound=tk.TOP)
btn_clear.grid(row=4, column=3, columnspan=2, padx=(10, 10), pady=(10, 10), sticky="nsew")

# Apply the theme
style = Style(theme='darkly')

# Run the Tkinter event loop
root.mainloop()

# Disconnect from the server
client.disconnect()
