# from PyPDF2 import PdfReader

# reader = PdfReader("PHYS172_F23_Syllabus&Schedule_2023-10-05.pdf")
# number_of_pages = len(reader.pages)
# page = reader.pages[0]
# page2 = reader.pages[1]

# text = page.extract_text()
# print(text)


# BEGIN: yz78abx1cde2
from PyPDF2 import PdfReader

reader = PdfReader("PHYS172_F23_Syllabus&Schedule_2023-10-05.pdf")
number_of_pages = len(reader.pages) - 3
for i in range(number_of_pages):
    page = reader.pages[i]
    text = page.extract_text()
    print(text)
 
# END: yz78abx1cde2
