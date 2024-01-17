"""
===============================================================================
ENGR 13300 Fall 2023

Program Description
    Takes user input about their major of interest and uses RAG (Retrieval Augmented Generation) to answer questions about the major
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

def majorChat():

    repeat = True

    while (repeat):
        valid = False

        while (valid == False):

            course = input("What major are you interested in learning more about? Type q to quit: ")

            if (course == 'q'):
                repeat = False
                break

            if course == "Computer Engineering" or course == "computer engineering" or course == "compe" or course == "comp e":
                loader = PyPDFLoader("Program_ Computer Engineering, BSCMPE - Purdue University - Acalog ACMS™.pdf")
                valid = True
            elif course == "Mechanical Engineering" or course == "mech e" or course == "meche" or course == "mechanical engineering":
                loader = PyPDFLoader("Program_ Mechanical Engineering, BSME - Purdue University - Acalog ACMS™.pdf")
                valid = True
            elif course == "Industrial Engineering" or course == "ind e" or course == "inde" or course == "industrial engineering":
                loader = PyPDFLoader("Program_ Industrial Engineering, BSIE - Purdue University - Acalog ACMS™.pdf")
                valid = True
            else:
                print("Sorry, we don't have that major in our database. Try computer, mechanical, or industrial engineering.")

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