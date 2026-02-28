import os 
from dotenv import load_dotenv

load_dotenv()

os.getenv("HF_TOKEN")

# from langchain_community.vectorstores import FAISS
# from langchain_huggingface import HuggingFaceEmbeddings

# embeddings = HuggingFaceEmbeddings(
#     model_name="all-MiniLM-L6-v2"
# )


# db_path = "embeddings"

# vectorstore = FAISS.load_local(
#     db_path,
#     embeddings,
#     allow_dangerous_deserialization=True
# )


# def search_data(query):
#     docs = vectorstore.similarity_search(query, k=3)
#     return docs

# result=search_data(query="what is the name of event")
# print(result)


#create the model

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
class ChatBot:
    store={}
    context_store={}
    def __init__(self):

        

        self.api_key=os.getenv("GROQ_API")
        self.model=ChatGroq(model="llama-3.1-8b-instant",api_key=self.api_key)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a context-based AI assistant. name is the Edwinova asiatnat 

                        Use ONLY the provided context and previous messages.
                        Do NOT hallucinate or use external knowledge.

                        If the answer is not in the context, say:
                        "The information is not available in the provided context."
                            
                        """),

            MessagesPlaceholder(variable_name="history"),

            ("human", "Context:\n{context}\n\nQuestion:\n{question}")
                        ])

    

    def chatbot(self,question,context,session_id):
        try:

            model=self.model
            prompt=self.prompt

            store=self.store
            context_store=self.context_store
            model=self.model

            if session_id not in context_store:
                context_store[session_id]=context
            
            self.saved_context=context_store[session_id]
            self.session_id=session_id

            def get_session_history(session_id:str)->BaseChatMessageHistory:
                if session_id not in store:
                    store[session_id]=InMemoryChatMessageHistory()
                return store[session_id]


            chain=prompt | model

            self.bot=RunnableWithMessageHistory(
                chain,
                get_session_history=get_session_history,
                input_messages_key="question",
                history_messages_key="history"
            )

            response=self.bot.invoke({"question": question, "context": self.saved_context},
                config={"configurable": {"session_id": self.session_id}}
            )

            return response.content
        except Exception as e:
            return {"expection":str(e)}

        
    def ask(self,question):
        response = self.bot.invoke(
            {"question": question, "context": self.saved_context},
            config={"configurable": {"session_id": self.session_id}}
        )

        return response.content

if __name__=="__main__":
    obj=ChatBot()
    print(obj.chatbot(question="what is my name" ,context="my name is kiran kumar s i am genertaive ai engineer" ,session_id="1"))

    while True:
        question=input("you :")
        response=obj.ask(question=question)
        print(response)
        
       
        
            