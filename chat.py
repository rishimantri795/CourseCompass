from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain import hub
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from prereq import requisites
from chatMajor import majorChat

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

#ask program catalog, ask course syllabus, find prerequisites, course compare, 

task = int(input("What do you want to do today? Enter '1' for Chatting with Program Catalogs, '2' for Chatting with a Course Syllabus, '3' for Finding Course Prerequisites \n"))

if (task == 1):
    majorChat()

elif (task == 2):
    requisites()

elif (task == 3):

    repeat = True

    while (repeat):

        course = input("What course are you interested in learning more about? Type q to quit: ")

        if (course == 'q'):
            repeat = False
            break

        if course == "PHYS 172" or course == "PHYS172" or course == 'phys 172' or course == 'phys172':
            loader = PyPDFLoader("PHYS172_F23_Syllabus&Schedule_2023-10-05.pdf")
            
        elif course == "MA 261" or course == "MA261" or course == 'ma 261' or course == 'ma261':
            loader = PyPDFLoader("syllabus_ma261_fa23.pdf")

        elif course == "CS 159" or course == "CS159" or course == 'cs 159' or course == 'cs159':
            loader = PyPDFLoader("syllabus.pdf")

        elif course == "ENGR 133" or course == "ENGR133" or course == 'engr 133' or course == 'engr133':
            loader = PyPDFLoader("ENGR 133_Fa23_Syllabus_V4.pdf")

        else:
            loader = PyPDFLoader("Program_ Computer Engineering, BSCMPE - Purdue University - Acalog ACMS™.pdf")

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