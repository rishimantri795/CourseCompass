"""
===============================================================================
ENGR 13300 Fall 2023

Program Description
    Uses Tkinter to display a GUI that allows the user to enter a class number and instructor name. The program then displays the grade distribution for that class and instructor

Assignment Information
    Assignment:     Individual Project
    Author:         Rishi Mantri, mantrir@purdue.edu
    Team ID:        LC4 - 10 

Contributor:    Name, login@purdue [repeat for each]
    My contributor(s) helped me:
    [ ] understand the assignment expectations without
        telling me how they will approach it.
    [ ] understand different ways to think about a solution
        without helping me plan my solution.
    [ ] think through the meaning of a specific error or
        bug present in my code without looking at my code.
    Note that if you helped somebody else with their code, you
    have to list that person as a contributor here as well.
    
ACADEMIC INTEGRITY STATEMENT
I have not used source code obtained from any other unauthorized
source, either modified or unmodified. Neither have I provided
access to my code to another. The project I am submitting
is my own original work.
===============================================================================
"""
import tkinter as tk
from tkinter import messagebox, ttk
import csv
import pandas as pd
import numpy as np
import re

class GUIApp:
    def __init__(self, master):
        self.master = master                        #master is the window
        self.master.title("Class Number GUI")

        self.label_dropdown = tk.Label(master, text="Choose Subject:")          #label for dropdown menu
        self.label_dropdown.pack()

        self.selected_option2 = tk.StringVar()                     #variable for dropdown menu
        self.dropdown = ttk.Combobox(master, textvariable=self.selected_option2, state="readonly")
        self.dropdown.pack()

        self.dropdown['values'] = tuple(self.get_subjects())            #populate dropdown menu with subjects

        # Create and set up widgets
        self.label = tk.Label(master, text="Enter Class Number (only Spring 2023):")
        self.label.pack()

        self.entry = tk.Entry(master)           #entry widget for class number
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

        with open('allgrades.csv', 'r') as file:            #get subjects from csv file
            reader = csv.reader(file)
            for row in reader:
                if row[0] == 'Subject' or row[0] == '':         #skip first row and empty rows
                    pass
                else:
                    subjects.append(row[0])                 #add subject to list
        return subjects

        # Replace this with your own logic for generating dropdown options
        
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

        with open('allgrades.csv', 'r') as file:            #get subjects from csv file
            j = 0
            mydata = []
            reader = csv.reader(file)                   #read csv file
            start_reading2 = False
            start2 = 0
            for row in reader:
                j += 1
                if start_reading2:
                    if row[0] != str(subject) and row[0] != '':         #stop reading when subject changes
                        break
                    mydata.append(row)          #add row to list
                elif row[0] == str(subject):
                    start2 = j
                    start_reading2 = True       #start reading when subject is found
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
                    if start_reading:           #start reading when subject is found
                        if row[2] != str(class_number) and row[2] != '':        #stop reading when class number changes
                            break
                        data.append(row)        #add row to list
                    elif row[2] == str(class_number):
                        start = i
                        start_reading = True
                        data.append(row)
            df = pd.DataFrame(data)                     
            df.to_csv('classdata.csv', index=False)         #write data to csv file

            if data == []:
                messagebox.showerror("Error", "Please enter a valid class number.")
                return 0,0,[]
                    
            return i-1,start,data
                  
        end,begin,mydata = read_csv_data(class_number)

        all_instructors = []
        gradeLevels = []
        dict_instructor_grades = {}
        with open('classdata.csv', 'r') as file:
            reader3 = csv.reader(file)
            all_instructors.append('All')
            for row in reader3:
                gradeLevels = []                #reset gradeLevels list
                if row[1] == '1':               #skip first row
                    pass
                else:
                    if row[8] not in all_instructors:           #add instructor to list
                        all_instructors.append(row[8])
                        for i in range(9,25):
                            if row[i] == '':
                                value = 0
                            else:
                                value = float(re.search(r'\d+\.\d+',row[i]).group())        #get grade value
                            gradeLevels.append(value)
                        dict_instructor_grades.update({row[8]:gradeLevels})            #add instructor and grade levels to dictionary         
        
        if instructor not in all_instructors:
            instructor = 'All'

        if instructor == 'All' or instructor == '':
            grades = np.zeros((16,end-begin+1))                 #create array to store grades
            index = -1
            with open('classdata.csv', 'r') as file:        
                reader = csv.reader(file)
                for row in reader:  
                    if row[1] == '1':                   #skip first row
                        pass
                    else:
                        index +=1
                        for i in range(9,25):       #loop through grade levels
                            if row[i] == '':
                                value = 0
                            else:
                                value = float(re.search(r'\d+\.\d+',row[i]).group())            #get grade value
                            grades[i-9][index] = value

            averages = np.zeros(16)             #create array to store averages
            for i in range(0,16):
                averages[i] = round(np.mean(grades[i]),2)       #calculate average for each grade level
            
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
                    if row[8] not in instructors:
                        instructors.append(row[8])
        
        # Replace this with your own logic for generating dropdown options
        return instructors

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()

#implement averages for each instructor