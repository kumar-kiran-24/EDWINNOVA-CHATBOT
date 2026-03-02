import os
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path

#load the data from the pdf 
from langchain_community.document_loaders import PyMuPDFLoader

loader=PyMuPDFLoader("data/RAG(1).pdf")
documnets=loader.load()



#decalre the embeddings models
from langchain_huggingface import HuggingFaceEmbeddings
embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
 

#call FAISS DB for tote the vectors data 
from langchain_community.vectorstores import FAISS

BASE_DIR=Path.cwd()
save=BASE_DIR/ "embeddings"
save.mkdir(parents=True, exist_ok=True)
db=FAISS.from_documents(documents=documnets,embedding=embeddings)
db.save_local(save)



