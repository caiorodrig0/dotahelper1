from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import DirectoryLoader, UnstructuredFileLoader, PyPDFLoader, PDFMinerLoader

import os

diretorio_pai = "C:\\Users\\caio.rodrigo.santos\\Downloads\\New folder (3)"


#loader = DirectoryLoader(diretorio_pai, glob="*.txt")
loader = PDFMinerLoader("C:\\Users\\caio.rodrigo.santos\\Downloads\\New folder (3)\\bbb.pdf")


docs = loader.load_and_split()
embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(docs, embeddings)
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2)
qa = RetrievalQA.from_chain_type(llm=llm,
                                    chain_type="stuff",
                                    retriever=docsearch.as_retriever())

#write a function that makes the ai learns about the text and generate more text

while True:
    question = input("\n> ")
    answer = qa.run(question)
    print(answer)
    if answer == "exit":
        break

