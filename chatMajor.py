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

        course = input("What major are you interested in learning more about? Type q to quit: ")

        if (course == 'q'):
            repeat = False
            break

        if course == "Computer Engineering" or course == "computer engineering" or course == "compe" or course == "comp e":
            loader = PyPDFLoader("Program_ Computer Engineering, BSCMPE - Purdue University - Acalog ACMS™.pdf")
        elif course == "Mechanical Engineering" or course == "mech e" or course == "meche" or course == "mechanical engineering":
            loader = PyPDFLoader("Program_ Mechanical Engineering, BSME - Purdue University - Acalog ACMS™.pdf")
        elif course == "Industrial Engineering" or course == "ind e" or course == "inde" or course == "industrial engineering":
            loader = PyPDFLoader("Program_ Industrial Engineering, BSIE - Purdue University - Acalog ACMS™.pdf")

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