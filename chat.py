"""
===============================================================================
ENGR 13300 Fall 2023

Program Description
    Takes input values for the task user wants to perform and calls the appropriate function. If user wants to chat with Class Requirements, it will perform RAG (Retrieval Augmented Generation) and answer questions about user classes

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
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain import hub
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from chatMajor import majorChat
from newReq import newReq
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")          #get API key from file

askagain = True

while (askagain):                                    #loop to keep asking questions

    task = (input("What do you want to do today? Enter '1' for Chatting with Major Requirements, '2' for Chatting with an Existing Course Syllabus, '3' for Exploring New Courses \n"))

    if (task == '1'):
        askagain = False
        majorChat()

    elif (task == '3'):
        askagain = False
        newReq()

    elif (task == '2'):

        askagain = False
        repeat = True

        while (repeat):
            valid = False
            while (valid == False):

                course = input("What course are you interested in learning more about? Type q to quit: ")

                if (course == 'q'):
                    repeat = False
                    break

                loader = None

                if course == "PHYS 172" or course == "PHYS172" or course == 'phys 172' or course == 'phys172':          #load syllabus based on course
                    loader = PyPDFLoader("PHYS172_F23_Syllabus&Schedule_2023-10-05.pdf")
                    valid = True
                    
                elif course == "MA 261" or course == "MA261" or course == 'ma 261' or course == 'ma261':
                    loader = PyPDFLoader("syllabus_ma261_fa23.pdf")
                    valid = True

                elif course == "CS 159" or course == "CS159" or course == 'cs 159' or course == 'cs159':
                    loader = PyPDFLoader("syllabus.pdf")
                    valid = True

                elif course == "ENGR 133" or course == "ENGR133" or course == 'engr 133' or course == 'engr133':
                    loader = PyPDFLoader("ENGR 133_Fa23_Syllabus_V4.pdf")
                    valid = True

                # elif course == 'apple':
                #     loader = PyPDFLoader("Apple Q4 2023 Earnings Call Transcript.pdf")
                #     valid = True   

                else:
                    print("Sorry, we don't have that course in our database. Try PHYS 172, MA 261, CS 159, or ENGR 133.")

                print("Loading documents...")


            if (course == 'q'):
                break


            #from https://python.langchain.com/docs/use_cases/question_answering/

            # Split documents
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
            splits = text_splitter.split_documents(loader.load())

            # Embed and store splits
            vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
            retriever = vectorstore.as_retriever()

            # Prompt
            # https://smith.langchain.com/hub/rlm/rag-prompt
            rag_prompt = hub.pull("rlm/rag-prompt")

            # LLM
            llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

            # RAG chain 
            rag_chain = {"context": retriever, "question": RunnablePassthrough()} | rag_prompt | llm

            again = True

            while (again):

                question = input("What's your question? Type q to quit: ")

                if (question == 'q'):
                    again = False
                    break
                
                result = rag_chain.invoke(question)

                print(result)
    else:
        print("Invalid input. Please enter a valid input.")


#loop to keep asking questions
#do user validation
#add more courses
#add more questions
#add more answers
#add more prompts
#figure out how to keep and return context
#program catalogs? 
#calendar integration
#Instructor Profiles