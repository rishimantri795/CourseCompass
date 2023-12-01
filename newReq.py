import requests
from bs4 import BeautifulSoup
import csv
import re

def newReq():

    yes = 'y'

    while(yes == 'y'):

        with open('ece-undergrad-courses.csv', newline='') as csvfile: 
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')

            csvfile.seek(0)
            
            course_name = input("What class do you want to know more about (enter course number?) Separate course numbers by comma if comparing multiple. Enter q to quit. \n")
            print("\n")

            if course_name == 'q':
                break

            class_names = [int(num) for num in course_name.split(',')]

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

            # else:        
            #     next(reader)
                
            #     for row in reader:
            #         if int(row[0]) == (class_name):
            #             name = (row[1])
            #             link = (row[4])
            #             break
            #     else:
            #         print("Class not found in the CSV file.")
            #         exit()

            #     response = requests.get(link)
            #     soup = BeautifulSoup(response.content, 'html.parser')

            #     target_element = soup.find(string="Requisites:")

            #     # Extract the text right after the target string
            #     if target_element:
            #         next_element = target_element.find_next('p')  # Assuming the text is in a <p> tag, you can adjust as needed
            #         if next_element:
            #             text_after_target = next_element.get_text()
            #             print("Prerequisites: " + text_after_target)
            #             numeric_part = ''
            #             numeric_part = ''.join(filter(str.isdigit, text_after_target))
            #             pattern = r'ECE (\d+)'

            #             matches = re.findall(pattern, text_after_target)
            #             csvfile.seek(0)
            #             for match in matches:
            #                 csvfile.seek(0)
            #                 for rows in reader:
            #                     if rows[0] == match:
            #                         names = rows[1]
            #                         print(names)
            #                         break
            #         else:
            #             print("No text found after the target string.")
            #     else:
            #         print("Target string not found in the HTML.")

            #     print("\n")
            #     yes = input("Do you want to know the prerequisites for another class? (y/n) ")






                


                