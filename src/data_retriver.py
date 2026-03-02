import os
from dotenv import load_dotenv

load_dotenv()

from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings
from fastembed import TextEmbedding


# ---------------------------
# Custom Embedding Class
# ---------------------------
class FastEmbedEmbeddings(Embeddings):
    def __init__(self):
        self.model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")

    def embed_documents(self, texts):
        return list(self.model.embed(texts))

    def embed_query(self, text):
        return list(self.model.embed([text]))[0]


# ---------------------------
# Data Retriever Class
# ---------------------------
class Dataretriver:
    def __init__(self):

        # ✅ use lightweight embeddings
        embeddings = FastEmbedEmbeddings()

        db_path = os.path.join(os.getcwd(), "embeddings")

        self.vectorstore = FAISS.load_local(
            db_path,
            embeddings,
            allow_dangerous_deserialization=True
        )

    def search_data(self, query):
        try:
            docs = self.vectorstore.similarity_search(query, k=3)

            # ✅ convert to text (IMPORTANT for LLM)
            return "\n\n".join([doc.page_content for doc in docs])

        except Exception as e:
            return {"error": str(e)}


# ---------------------------
# Test
# ---------------------------
if __name__ == "__main__":
    obj = Dataretriver()
    result = obj.search_data(query="what is this document contains")
    print(result)