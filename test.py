import tkinter as tk
from tkinter import messagebox, ttk
import csv
import pandas as pd
import numpy as np
import re

class GUIApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Class Number GUI")

        # Create and set up widgets
        self.label = tk.Label(master, text="Enter Class Number:")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.button = tk.Button(master, text="Submit", command=self.show_outputs)
        self.button.pack()

        self.output_listbox = tk.Listbox(master)
        self.output_listbox.pack()

        self.label_dropdown = tk.Label(master, text="Choose from the list:")
        self.label_dropdown.pack()

        # Create a StringVar to store the selected option
        self.selected_option = tk.StringVar()

        # Create a drop-down list
        self.dropdown = ttk.Combobox(master, textvariable=self.selected_option, state="readonly")
        self.dropdown.pack()

    def show_outputs(self):
        # Get class number from the entry widget
        class_number = self.entry.get()

        # Validate input
        if not class_number.isdigit():
            messagebox.showerror("Error", "Please enter a valid class number.")
            return

        # Clear previous outputs and options
        self.output_listbox.delete(0, tk.END)
        self.dropdown['values'] = ()

        # Generate and display list of outputs
        outputs = self.generate_outputs(int(class_number))
        for output in outputs:
            self.output_listbox.insert(tk.END, output)

        # Populate drop-down list with options
        self.dropdown['values'] = tuple(self.generate_dropdown_options(class_number))

    def generate_outputs(self, class_number):

        def read_csv_data(class_number):
            i = 0
            start = 0
            with open('ece_gradeDistro (1).csv', 'r') as file:
                reader = csv.reader(file)
                data = []
                start_reading = False

                for row in reader:
                    i += 1
                    if start_reading:
                        if row[1] != str(class_number) and row[1] != '':
                            break
                        data.append(row)
                    elif row[1] == str(class_number):
                        start = i
                        start_reading = True
                        data.append(row)
            df = pd.DataFrame(data)
            df.to_csv('classdata.csv', index=False)
                    
                    
            return i-1,start,data

        end,begin,mydata = read_csv_data(class_number)
        #print(f"The row numbers occupied by class number {class_number} is: {begin} to {end}")
        grades = np.zeros((16,end-begin+1))

        index = -1
        with open('classdata.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                
                if row[1] == '1':
                    pass
                else:
                    index +=1
                    for i in range(8,24):
                        if row[i] == '':
                            value = 0
                        else:
                            value = float(re.search(r'\d+\.\d+',row[i]).group())

                        grades[i-8][index] = value

                        #grades[i-8][0] = float(row[i].strip('.%'))                    
        averages = np.zeros(16)
        for i in range(0,16):
            averages[i] = round(np.mean(grades[i]),2)
        
        dict = {'A': averages[0], 'A-': averages[1], 'A+': averages[2], 'AU': averages[3], 'B': averages[4], 'B-': averages[5], 'B+': averages[6], 'C': averages[7], 'C-': averages[8], 'C+': averages[9], 'D': averages[10], 'D-': averages[11], 'D+': averages[12], 'E': averages[13], 'F': averages[14], 'I': averages[15]}

        for i in dict:
            print(f"The average grade for {i} is {dict[i]}%")
        
        return [f"Grade {i} : {dict[i]}%" for i in dict]

    def generate_dropdown_options(self,class_number):

        instructors = [] 

        with open('classdata.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == '1':
                    pass
                else:
                    if row[7] not in instructors:
                        instructors.append(row[7])
        
        # Replace this with your own logic for generating dropdown options
        return instructors

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()








        
