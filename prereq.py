import requests
from bs4 import BeautifulSoup
import csv
import re

def requisites():

    yes = 'y'

    while(yes == 'y'):

        class_name = input("What class do you want to know more about (enter course number?) ")

        with open('ece-undergrad-courses.csv', newline='') as csvfile: 
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        
            for row in reader:
                if row[0] == class_name:
                    name = (row[1])
                    link = (row[4])
                    break
            else:
                print("Class not found in the CSV file.")
                exit()

            response = requests.get(link)
            soup = BeautifulSoup(response.content, 'html.parser')

            target_element = soup.find(string="Requisites:")

            # Extract the text right after the target string
            if target_element:
                next_element = target_element.find_next('p')  # Assuming the text is in a <p> tag, you can adjust as needed
                if next_element:
                    text_after_target = next_element.get_text()
                    print(text_after_target)
                    numeric_part = ''
                    numeric_part = ''.join(filter(str.isdigit, text_after_target))
                    pattern = r'ECE (\d+)'

                    matches = re.findall(pattern, text_after_target)
                    csvfile.seek(0)
                    for match in matches:
                        csvfile.seek(0)
                        for rows in reader:
                            if rows[0] == match:
                                names = rows[1]
                                print(names)
                                break
                else:
                    print("No text found after the target string.")
            else:
                print("Target string not found in the HTML.")

            print("\n")
            yes = input("Do you want to know the prerequisites for another class? (y/n) ")
    
#ask for course chatting or course exploration. In course exploration, you can explore multiple courses and compare them. 
#you can get details like the prerequisites, the number of credits, description, required textbooks, etc.
