import os 
from dotenv import load_dotenv

load_dotenv()

os.getenv("HF_TOKEN")

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


class Dataretriver:
    def __init__(self):

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )


        db_path = os.path.join(os.getcwd(), "embeddings")

        self.vectorstore = FAISS.load_local(
            db_path,
            embeddings,
            allow_dangerous_deserialization=True
        )


    def search_data(self,query):
        try:

            
            docs = self.vectorstore.similarity_search(query, k=3)
            return docs
        except Exception as e:
            return {"error":str(e)}

if __name__=="__main__":
    obj=Dataretriver()
    result=obj.search_data(query="what is this document conatins")
    print(result)
