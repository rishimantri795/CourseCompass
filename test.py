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

        self.label_dropdown = tk.Label(master, text="Choose Subject:")
        self.label_dropdown.pack()

        self.selected_option2 = tk.StringVar()
        self.dropdown = ttk.Combobox(master, textvariable=self.selected_option2, state="readonly")
        self.dropdown.pack()

        self.dropdown['values'] = tuple(self.get_subjects())

        # Create and set up widgets
        self.label = tk.Label(master, text="Enter Class Number:")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.button = tk.Button(master, text="Submit", command=self.show_outputs)
        self.button.pack()

        self.label_dropdown = tk.Label(master, text="Choose instructor from the list (will populate on submission):")
        self.label_dropdown.pack()

        # Create a StringVar to store the selected option
        self.selected_option = tk.StringVar()

        # Create a drop-down list
        self.dropdown = ttk.Combobox(master, textvariable=self.selected_option, state="readonly")
        self.dropdown.pack()

        label = tk.Label(text="Course Grade Distribution:")
        label.pack()

        self.output_listbox = tk.Listbox(master)
        self.output_listbox.pack()

    def get_subjects(self):
        subjects = []

        with open('allgrades.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == 'Subject' or row[0] == '':
                    pass
                else:
                    subjects.append(row[0])
        return subjects

        # Replace this with your own logic for generating dropdown options
        return subjects
        
    def show_outputs(self):
        # Get class number from the entry widget
        class_number = self.entry.get()
        instructor = self.selected_option.get()
        subject = self.selected_option2.get()

        # Validate input
        if not class_number.isdigit():
            messagebox.showerror("Error", "Please enter a valid class number.")
            return

        # Clear previous outputs and options
        self.output_listbox.delete(0, tk.END)
        self.dropdown['values'] = ()

        # Generate and display list of outputs
        outputs = self.generate_outputs(int(class_number), instructor, subject)
        for output in outputs:
            self.output_listbox.insert(tk.END, output)

        # Populate drop-down list with options
        self.dropdown['values'] = tuple(self.generate_dropdown_options(class_number))

    def generate_outputs(self, class_number, instructor,subject):

        with open('allgrades.csv', 'r') as file:
            j = 0
            mydata = []
            reader = csv.reader(file)
            start_reading2 = False
            start2 = 0
            for row in reader:
                j += 1
                if start_reading2:
                    if row[0] != str(subject) and row[0] != '':
                        break
                    mydata.append(row)
                elif row[0] == str(subject):
                    start2 = j
                    start_reading2 = True
                    mydata.append(row)
        df = pd.DataFrame(mydata)
        df.to_csv('subjectdata.csv', index=False)


          
        def read_csv_data(class_number):
            i = 0
            start = 0
            with open('subjectdata.csv', 'r') as file:
                reader = csv.reader(file)
                data = []
                start_reading = False

                for row in reader:
                    i += 1
                    if start_reading:
                        if row[2] != str(class_number) and row[2] != '':
                            break
                        data.append(row)
                    elif row[2] == str(class_number):
                        start = i
                        start_reading = True
                        data.append(row)
            print(data)
            df = pd.DataFrame(data)
            df.to_csv('classdata.csv', index=False)
                    
            return i-1,start,data
                  
        end,begin,mydata = read_csv_data(class_number)

        all_instructors = []
        gradeLevels = []
        dict_instructor_grades = {}
        with open('classdata.csv', 'r') as file:
            reader3 = csv.reader(file)
            all_instructors.append('All')
            for row in reader3:
                gradeLevels = []
                if row[1] == '1':
                    pass
                else:
                    if row[8] not in all_instructors:
                        all_instructors.append(row[8])
                        for i in range(9,25):
                            if row[i] == '':
                                value = 0
                            else:
                                value = float(re.search(r'\d+\.\d+',row[i]).group())
                            gradeLevels.append(value)
                        dict_instructor_grades.update({row[8]:gradeLevels})  
            print(dict_instructor_grades)

        
        if instructor not in all_instructors:
            instructor = 'All'

        if instructor == 'All' or instructor == '':
            grades = np.zeros((16,end-begin+1))
            index = -1
            with open('classdata.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[1] == '1':
                        pass
                    else:
                        index +=1
                        for i in range(9,25):
                            if row[i] == '':
                                value = 0
                            else:
                                print(row[i])
                                value = float(re.search(r'\d+\.\d+',row[i]).group())

                            grades[i-9][index] = value

            averages = np.zeros(16)
            for i in range(0,16):
                averages[i] = round(np.mean(grades[i]),2)
            
            dict = {'A': averages[0], 'A-': averages[1], 'A+': averages[2], 'AU': averages[3], 'B': averages[4], 'B-': averages[5], 'B+': averages[6], 'C': averages[7], 'C-': averages[8], 'C+': averages[9], 'D': averages[10], 'D-': averages[11], 'D+': averages[12], 'E': averages[13], 'F': averages[14], 'I': averages[15]}
            
            return [f"Grade {i} : {dict[i]}%" for i in dict]
        
        else:
            grades = dict_instructor_grades[instructor]
            averages = grades
            dict = {'A': averages[0], 'A-': averages[1], 'A+': averages[2], 'AU': averages[3], 'B': averages[4], 'B-': averages[5], 'B+': averages[6], 'C': averages[7], 'C-': averages[8], 'C+': averages[9], 'D': averages[10], 'D-': averages[11], 'D+': averages[12], 'E': averages[13], 'F': averages[14], 'I': averages[15]}
            
            return [f"Grade {i} : {dict[i]}%" for i in dict]

    def generate_dropdown_options(self,class_number):

        instructors = [] 

        with open('classdata.csv', 'r') as file:
            reader = csv.reader(file)
            instructors.append('All')
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


#implement averages for each instructor, implement for all Purdue classes/departments