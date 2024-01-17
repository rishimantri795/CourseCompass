"""
===============================================================================
ENGR 13300 Fall 2023

Program Description
    Asks user input for the ECE course number and displays the course description, prerequisites, required and recommended textbooks
    
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

import requests
from bs4 import BeautifulSoup
import csv
import re
from distributions import GUIApp
import tkinter as tk
import pandas as pd

def newReq():

    yes = 'y'

    while(yes == 'y'):

        with open('ece-undergrad-courses.csv', newline='') as csvfile: 
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')

            valid = False

            while (valid == False):

                csvfile.seek(0)
                course_name = input("What class do you want to know more about (enter an ECE course number)? Enter 'd' for grade distributions by course & instructor. Enter q to quit. \n")
                print("\n")

                if course_name == 'd':
                    root = tk.Tk()
                    app = GUIApp(root)
                    root.mainloop()
                    break
                    
                elif course_name == 'q':
                    break

                elif course_name.isalpha():
                    print("Please enter a valid class number.")
                    valid = False

                elif course_name.isnumeric() == False:
                    print("Please enter a valid class number.")
                    valid = False

                else:

                    class_names = [int(num) for num in course_name.split(',')]

                    ececourses = pd.read_csv('ece-undergrad-courses.csv')
                    ececourses = ececourses['Course Number'].tolist()
                    for i in class_names:
                        if i not in ececourses:
                            print(f"ECE {i} is not a valid class.")
                            valid = False
                            break
                        else:
                            valid = True

            if course_name == 'q':
                break
            if course_name == 'd':
                break

            i = 0

            for i in range(len(class_names)):

                csvfile.seek(0)
                next(reader)
                
                for row in reader:
                    if int(row[0]) == int(class_names[i]):
                        name = row[1]
                        link = row[4]
                        break                  
                else:                           
                    print(f"ECE {class_names[i]} is not a valid class.")
                    exit()  

                response = requests.get(link)
                soup = BeautifulSoup(response.content, 'html.parser')

                target_element4 = soup.find(string="Catalog Description:")
                if target_element4:
                    next_element4 = target_element4.find_next('p')

                target_element = soup.find(string="Requisites:")
                # Extract the text right after the target string
                if target_element:
                    next_element = target_element.find_next('p')

                target_element2 = soup.find(string="Required Text(s):")
                if target_element2:
                    next_element2 = target_element2.find_next('li')

                target_element3 = soup.find(string="Recommended Text(s):")
                if target_element3:
                    next_element3 = target_element3.find_next('p')

                print("Class: ECE " + str(class_names[i]) + " " + name)
                print("Description: " + next_element4.get_text())
                print("Prerequisites: " + next_element.get_text())
                print("Required Text(s): " + next_element2.get_text())
                print("Recommended Text(s): " + next_element3.get_text() + "\n")




                


                